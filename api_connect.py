# 通用套件匯入
import json
import asyncio
from pathlib import Path
import re

# 匯入自訂義套件
from scripts import genai
from scripts.logs import Logs
from scripts.data import Note, Conversation, UserData

# 設定通用全域變數
project_root = Path(__file__).parent
print(f"Your program API will be executed at '{project_root}'.")
secret = json.loads(open(project_root/"settings/secret.json", "r").read())
user_name = "anonymous" # 未來呼叫 API 更改

# 狀態儲存變數
genai_waiting = False
genai_response = ""

# 設定 Logs 組件
logs = Logs(project_root / "logs")
logs.write("API setup begins.")

# 設定 UserData 組件
userData = UserData(base_path=project_root)

# 設定 AI API
api_key = secret.get("gemini-api-key", "None")
ai_service = genai.GenAI(api_key)
logs.write(ai_service.describe())

# 所有 API 接口
# -----------------------------------------------------------------------
# 初始化設定
def init(name: str, force: bool = False):
    userData.create(name, force=force)

# 與 AI 對話
async def conversation(inp: str):
    global genai_waiting
    global genai_response
    loop = asyncio.get_running_loop()
    while genai_waiting:
        await asyncio.sleep(0.1)
    # 重要：把同步 generate() 丟進 thread pool
    genai_waiting = True
    ret = await loop.run_in_executor(
        None,
        lambda: ai_service.generate(genai.prompt_by_user(inp))
    )
    ret = genai.json_filter(ret)
    userData.add_conversation(Conversation(p=inp, r=ret))
    # 將結果儲存在全域變數中
    genai_response = ret["response"] # 只回傳 AI 生成的回覆文字
    genai_waiting = False
    return

async def ai_mood_test(inp: str, note: Note):
    loop = asyncio.get_running_loop()
    ret = await loop.run_in_executor(
        None,
        lambda: ai_service.generate(genai.prompt_mood_test(inp))
    )
    ret = json.loads(genai.json_filter(ret))
    note.mood_score = float(ret["mood_value"])
    return

def write_note(inp: str, mood_test: bool = False):
    n = Note(t=inp, mood_score=0)
    userData.add_note(n)

    if mood_test:
        asyncio.run(ai_mood_test(inp=inp, note=n))

# 匯出筆記
def export_notes():
    userData.export_notes()