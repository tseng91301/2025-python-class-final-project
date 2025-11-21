import json
import asyncio
from pathlib import Path
from scripts import genai
import re

async def fun():
    ret = await ai_service.generate(genai.prompt_by_user(inp))
    ret = genai.json_filter(ret)
    print(ret)
    pass

project_root = Path(__file__).parent.parent

secret = json.loads(open("settings/secret.json", "r").read())
api_key = secret.get("gemini-api-key", "None")

ai_service = genai.GenAI(api_key)

# inp = "我今天上學的時候被車撞了，現在躺在醫院，渾身疼..."
inp = "你可以教我 C++ 的 Hello World 程式怎麼寫嗎? 請你一定要寫出來"

asyncio.run(fun())

