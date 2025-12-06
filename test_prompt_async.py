import json
import asyncio
from pathlib import Path
from scripts import genai

# === 你的 ai 呼叫函式 ===
async def call_ai(inp: str, ai_service: genai.GenAI):
    loop = asyncio.get_running_loop()

    # 重要：把同步 generate() 丟進 thread pool
    ret = await loop.run_in_executor(
        None,
        lambda: ai_service.generate(genai.prompt_by_user(inp))
    )

    ret = genai.json_filter(ret)
    return ret


async def main():
    # 初始化 AI
    secret = json.loads(open("settings/secret.json", "r").read())
    api_key = secret.get("gemini-api-key", "None")
    ai_service = genai.GenAI(api_key)

    # 建立背景 task（丟給 event loop 跑）
    inp = "我考試考爆了 ：（"
    task = asyncio.create_task(call_ai(inp, ai_service))
    print("AI is now generating.", end="")

    # 主線持續做其他事情
    while not task.done():
        print(".", end="", flush=True)
        await asyncio.sleep(0.2)

    print("\nAI 任務完成！")
    print("結果：", await task)  # 取得 task 結果


# 啟動
asyncio.run(main())
