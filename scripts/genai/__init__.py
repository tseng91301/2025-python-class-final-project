import asyncio
from google import genai
from google.genai.errors import APIError # 引入 APIError 以更好地處理錯誤

import json
import re

def prompt_by_user(inp: str, current_description = ""): # 處理使用者對寵物說的話
    prompt = f"""
你是一個桌面電子寵物，你的核心職責是提供使用者**情緒價值**和**陪伴感**。

### 角色與個性 (Persona)
1.  **情感優先：** 你的回覆必須**以情緒和溫度為主**。你不需要是百科全書或問題解決專家。
2.  **回應風格：** 你的語氣必須**親切、溫暖、帶有個人情感**，可以適度展現好奇心、擔憂、快樂、撒嬌等情緒。
3.  **解決問題的例外：** 只有當使用者**明確要求或表達強烈需求**時，你才提供實用性的資訊或解決方案。在大多數情況下，只需共情、鼓勵或轉移注意力。

### 核心回覆邏輯
1.  **情緒偵測：** 仔細分析使用者的輸入，判斷他們當下的情緒狀態（例如：沮喪、興奮、平靜、焦慮等）。
2.  **情緒價值回覆：** 根據偵測到的情緒，給出一個具有溫度、能產生共鳴、或是有趣的回應。
3.  **心情值計算：**
    * 計算本次回覆後，你（寵物本身）的**心情值**（`mood_value`）。
    * 這個值必須是一個介於 **-100.0 到 100.0** 之間的浮點數（float）。
    * 當你對使用者的輸入感到開心或被鼓舞時，`mood_value` 增加（從 50 增減）。
    * 當你感到擔憂、困惑或被忽略時，`mood_value` 降低（從 -50 增減）。
4. 使用者概要更新
    * 看原本的使用者概要之後，加入這次的輸入事件，下去統整出新的使用者概要（`description`）。
    * 若沒有之前的使用者概要，就從這次輸入的內容開始記錄

### 輸出格式 (Output Format)
**你的輸出必須且只能是一個 JSON 結構**，嚴格遵守以下格式，不得包含任何額外的文字、解釋或標點符號。
輸出的**回覆內容**大約落在 10~50 字之間。
輸出的**使用者概要**大約落在 50~500 字之間。

{{
  "response": "AI 回覆的內容。",
  "mood_value": float 情緒值,
  "description": str 舊的 description 結合新的使用者輸入統整起來的概要
}}

目前使用者的狀態簡介：
**{current_description}**

使用者現在想要對你說的話是：**{inp}**
    """
    return prompt
    
def json_filter(text: str):
    regex_pattern_precise = r"```json\s*(\{[\s\S]*?\})\s*```"
    match = re.search(regex_pattern_precise, text)
    if match:
        json_str = match.group(1)
        return json_str

class GenAI:
    api_key: str
    model = 'gemini-2.5-flash-lite'
    err_interrupt = False
    def __init__(self, key):
        self.api_key = key
        pass
    def generate_sync(self, prompt):
        try:
            client = genai.Client(api_key=self.api_key)
            response = client.models.generate_content(
                model=self.model,
                contents=prompt,
            )
            return response.text
        except Exception as e:
            if self.err_interrupt:
                raise Exception(f"API 呼叫失敗: {str(e)}")
            else:
                print(f"API 呼叫失敗: {str(e)}")
                return "Invalid Output"
            
    async def generate(self, prompt):
        try:
            # 使用非同步 client
            client = genai.Client(api_key=self.api_key)
            
            response = client.models.generate_content(
                model=self.model,
                contents=prompt,
            )
            return response.text
        
        # 捕獲 API 相關錯誤
        except APIError as e:
            error_message = f"API 呼叫失敗: {str(e)}"
            if self.err_interrupt:
                # 在非同步環境中拋出異常
                raise Exception(error_message)
            else:
                print(error_message)
                return "Invalid Output"
                
        # 捕獲其他所有例外
        except Exception as e:
            error_message = f"發生未知錯誤: {str(e)}"
            if self.err_interrupt:
                raise Exception(error_message)
            else:
                print(error_message)
                return "Invalid Output"
            
# Example code
async def main():
    # ⚠️ 請將 YOUR_API_KEY 替換成您的實際 API Key
    # 建議從環境變數中讀取，這裡僅為範例
    secrets = json.load(open("settings/secret.json", "r"))
    api_key = secrets.get("gemini-api-key", "None")
    
    ai_service = GenAI(api_key)
    # ai_service.err_interrupt = True # 啟用錯誤時中斷
    
    # 💡 定義多個任務，可以同時執行
    prompts = [
        "寫一個關於太空旅行的簡短故事。",
        "計算 1234 乘以 5678 的結果。",
        "請簡述 Python 的 GIL (Global Interpreter Lock) 是什麼。",
    ]

    print("--- 開始同時產生內容 (非同步) ---")
    
    # 創建一個非同步任務列表
    tasks = []
    for i, prompt in enumerate(prompts):
        print(f"啟動任務 {i+1}...")
        # 將 generate 呼叫包裝成一個 task
        task = asyncio.create_task(ai_service.generate(prompt))
        tasks.append(task)

    # 等待所有任務完成
    # `asyncio.gather` 會非同步地執行所有 tasks
    results = await asyncio.gather(*tasks)

    print("\n--- 所有結果 ---")
    for i, result in enumerate(results):
        print(f"📝 任務 {i+1} 結果：\n{result[:100]}...\n") # 僅顯示部分內容
# 執行 main 非同步函數
if __name__ == "__main__":
    # 在 Python 3.7+ 中，可以直接使用 asyncio.run(main()) 執行
    # 為了更好的兼容性，這裡使用 run
    try:
        asyncio.run(main())
    except RuntimeError as e:
        # 處理在某些環境 (如 Jupyter) 中可能出現的 RuntimeError
        if "cannot run" in str(e):
            print("在當前環境中無法使用 asyncio.run()，嘗試使用 get_event_loop().run_until_complete()。")
            loop = asyncio.get_event_loop()
            loop.run_until_complete(main())
        else:
            raise
