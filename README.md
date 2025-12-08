## 專案 WorkFlow (僅供參考)

```mermaid
---
config:
  layout: elk
---
flowchart TB
 subgraph s1["前後端互動接口"]
        n4["api.conversation"]
        n5["api.write_note"]
        n6["api.get_all_notes"]
        n7["api.export_notes"]
  end
 subgraph s2["資料貯存位置"]
        n8["Notes"]
        n9["Conversations"]
  end
 subgraph s3["AI 互動接口"]
        n10["Get Mood Score"]
        n11["Chat Responser"]
  end
 subgraph s4["暫存區"]
        n12["genai_waiting: bool"]
        n13["genai_response: str"]
        n14["genai_mood_value: str"]
  end
 subgraph s5["前端畫面"]
        n16["日記視窗"]
        n1["聊天室視窗"]
        n17["桌寵本體"]
  end
    n1 -- 使用者欲與 AI 互動 --> n4
    n16 -- 撰寫日記 --> n5
    n16 -- 取得筆記列表 --> n6
    n4 --> n11
    n5 --> n10
    n5 -- 儲存日記資料 --> n8
    n11 -- 結果貯存 --> n9
    n8 -- 資料庫回傳筆記列表 （傳統 json 形式） --> n16
    n8 --> n7
    n10 -- 更新 Note 的情緒分數 --> n8
    n11 -- 更新暫存區資訊 --> s4
    s4 -- 將資訊放到畫面的聊天室 --> n1
    n7 -- 儲存 --> n15["外部檔案"]
    n16 -. 尚未實做 .-x n7

    n4@{ shape: rounded}
    n5@{ shape: rounded}
    n6@{ shape: rounded}
    n7@{ shape: rounded}
    n8@{ shape: cyl}
    n9@{ shape: cyl}
    n11@{ shape: rect}
    n13@{ shape: rect}
    n14@{ shape: rect}
    n16@{ shape: rounded}
    n1@{ shape: rounded}
    n17@{ shape: rounded}
    n15@{ shape: card}
     n4:::APIFunction
     n5:::APIFunction
     n6:::APIFunction
     n7:::APIFunction
     n8:::Sky
     n9:::Sky
     n10:::API
     n11:::API
     n12:::Sky
     n13:::Sky
     n14:::Sky
     n16:::Class_01
     n1:::Class_01
     n17:::Class_01
    classDef Aqua stroke-width:1px, stroke-dasharray:none, stroke:#46EDC8, fill:#DEFFF8, color:#378E7A
    classDef APIFunction stroke-width:4px, stroke-dasharray:0, stroke:#FF6D00, fill:#FFE0B2, color:#FF6D00
    classDef API Function stroke-width:4px, stroke-dasharray:0, stroke:#FF6D00, fill:#FFE0B2, color:#FF6D00
    classDef Sky stroke-width:1px, stroke-dasharray:none, stroke:#374D7C, fill:#E2EBFF, color:#374D7C
    classDef Class_01 stroke-width:4px, stroke-dasharray:0, stroke:#2962FF, fill:#BBDEFB, color:#2962FF
    style s1 stroke:#000000

```

## 初次設定專案
### 安裝所需的函式庫/模組
```shell
# Windows 系統執行下面命令
pip install -r requirements.txt

# Linux 發行版系統執行下面命令
pip install -r requirements-linux.txt
```
### 設定 secret key
1. 在專案根目錄新建 `settings/secret.json`
2. 取得一個 Gemini 的 API KEY
3. 將 API KEY 的字串放到 `settings/secret.json` 中
  ```json
  {
      "gemini-api-key": "AIxxxxxxxxxxx..."
  }
  ```

## 如何使用
* 在終端機中執行 `python main.py` 即可跳出互動視窗

## 後端處理程式
> 後端負責的是資料儲存、整合資訊與生程式 AI 互動。
### 主要使用的 API
#### 生成式 AI 互動套件
* 套件名稱: `genai`
* 套件位置: `scripts/genai/`
* 套件功能: 
  1. 將一段文字傳送給 Gemini 的生成式 AI 並且回傳其回覆
  2. 使用一些特定的功能函式(例如叫 AI 執行特定作業等)

#### 資料儲存套件
* 套件名稱: `data`
* 套件位置: `scripts/data`
* 套件功能:
  1. 讀取/儲存目前使用者的狀態、所有寫過的筆記和與 AI 的互動

#### Log 紀錄套件
* 套件名稱: `logs`
* 套件位置: `scripts/logs`
* 套件功能: 
  1. 寫入所有系統運行的紀錄/錯誤輸出等

### UserData
#### 儲存資料結構
```json
{
  "name": str,
  "current_mood_score": float(min=-100, max=100),
  "description": str(不超過 500 字，從使用者的歷史筆記去簡要紀錄),
  "notes": [
    {
      "dateTime": str(紀錄筆記的日期、時間),
      "text": str(紀錄的內容),
      "mood_score": float(min=-100, max=100)
    },
    ...
  ],
  "conversations": [
    {
      "dateTime": str(紀錄對話的日期、時間),
      "prompt": str(使用者的輸入),
      "ai_return": {
        "response": str(AI 的回覆),
        "mood_value": float(AI 針對使用者目前狀態給出的情緒分數),
        "description": str(AI 針對使用者先前狀態以及此對話綜合起來的簡述)
      }
    },
    ...
  ]

}
```

## 測試後端程式的運作
> 參考 `/test_api.py` 內的程式碼，將其複製到 REPL 中逐行執行，觀察結果
