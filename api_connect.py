# 通用套件匯入
import json
import asyncio
import threading
from pathlib import Path
import re

# 匯入自訂義套件
from scripts import genai
from scripts.logs import Logs, LOG_LEVEL_INFO, LOG_LEVEL_WARNING, LOG_LEVEL_ERROR
from scripts.data import Note, Conversation, UserData

# 設定通用全域變數
project_root = Path(__file__).parent
print(f"Your program API will be executed at '{project_root}'.")
secret = json.loads(open(project_root/"settings/secret.json", "r", encoding="utf-8").read())
user_name = "anonymous"  # 未來呼叫 API 更改

# 狀態儲存變數
genai_waiting = False
genai_response = ""
genai_mood_value = 0.0

# 設定 Logs 組件
logs = Logs(project_root / "logs")
logs.write("API setup begins.")

# 設定 UserData 組件
userData = UserData(base_path=project_root)

# 設定 AI API
api_key = secret.get("gemini-api-key", "None")
ai_service = genai.GenAI(api_key)
logs.write(ai_service.describe())

# ============================================================
# 背景 Event Loop 設定
# ============================================================
_background_loop = asyncio.new_event_loop()

def _loop_runner(loop: asyncio.AbstractEventLoop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

_loop_thread = threading.Thread(target=_loop_runner, args=(_background_loop,), daemon=True)
_loop_thread.start()
# 以上：匯入這隻檔案時就會啟動一個背景 event loop

# ============================================================
# API 接口
# ============================================================

# 初始化設定
def init(name: str, force: bool = False):
    global genai_mood_value
    userData.create(name, force=force)
    # 讀取先前的情緒分數
    if len(userData.conversations) > 0:
        genai_mood_value = userData.conversations[-1].ai_return["mood_value"]
    elif len(userData.notes) > 0:
        genai_mood_value = userData.notes[-1].mood_score

# ============================================================
# 非同步 AI 對話（主 async function）
# ============================================================

async def conversation(inp: str):
    global genai_waiting
    global genai_response
    global genai_mood_value

    loop = asyncio.get_running_loop()

    # 如果上一個還沒完成，等一下 
    while genai_waiting:
        await asyncio.sleep(0.1)

    logs.write(f"[conversation] Start asking AI, q='{inp}'")
    genai_waiting = True

    try:
        # 丟 thread pool：不會阻塞 event loop
        ret = await loop.run_in_executor(
            None,
            lambda: ai_service.generate(genai.prompt_by_user(inp))
        )
        ret = json.loads(genai.json_filter(ret))
    except Exception as e:
        logs.write(f"[conversation] ERROR: {repr(e)}")
        ret = {
            "response": "因為一些技術問題，無法取得 AI 回應",
            "mood_value": 0,
            "description": "N/A"
        }

    # 存 conversation
    userData.add_conversation(Conversation(p=inp, r=ret))

    # 回存
    genai_response = ret["response"]
    genai_mood_value = ret["mood_value"]

    logs.write(f"[conversation] AI answered q='{inp}'")
    genai_waiting = False
    return


# ============================================================
# 在背景 event loop 執行對話（立即返回，不阻塞 REPL）
# ============================================================

def conversation_bg(inp: str):
    """非同步啟動 AI 對話，但不等待結果，立刻返回。"""
    global genai_waiting

    # 如果 AI 正忙就拒絕新的要求
    if genai_waiting:
        logs.write("[conversation_bg] AI is busy, skip new request.")
        return False

    # 建立 background 版本
    fut = asyncio.run_coroutine_threadsafe(
        conversation(inp),
        _background_loop
    )

    # 設定錯誤 callback
    def _cb(f):
        try:
            f.result()
        except Exception as e:
            logs.write(f"[conversation_bg] ERROR: {repr(e)}")

    fut.add_done_callback(_cb)

    return True

# 情緒分析
async def ai_mood_test(inp: str, note: Note):
    try:
        logs.write(f"Beginning AI Mood Test, inp = '{inp}'")
        loop = asyncio.get_running_loop()
        ret = await loop.run_in_executor(
            None,
            lambda: ai_service.generate(genai.prompt_mood_test(inp))
        )
        ret = json.loads(genai.json_filter(ret))  # 或 json.loads(...) 看你實作
        note.mood_score = float(ret["mood_value"])
        userData.save()
        logs.write(f"AI Mood Test Completed, inp = '{inp}'")
    except Exception as e:
        print("Got some errors during execution, see log file.")
        logs.write(f"ai_mood_test exception: {repr(e)}", level=LOG_LEVEL_ERROR)

def get_all_notes() -> list:
    return [n.output() for n in userData.notes]

def write_note(inp: str, mood_test: bool = False):
    n = Note(t=inp, mood_score=0)
    logs.write(f"Note added to userData: {inp}")
    userData.add_note(n)  # 先把 note 存起來（mood_score = 0）

    if mood_test:
        # 把 ai_mood_test 排進「背景 event loop」中執行
        asyncio.run_coroutine_threadsafe(
            ai_mood_test(inp=inp, note=n),
            _background_loop
        )
        # 不要 await，直接 return，REPL 立刻可以做下一件事

# 匯出筆記
def export_notes():
    userData.export_notes()
