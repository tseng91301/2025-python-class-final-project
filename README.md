```mermaid
---
config:
  layout: dagre
---
flowchart TB
    C{"Start"} -- Initialize --> E["Log System"] & n1["Message Handler"] & n4["Mood System"]
    n2["Got Message Input"] -.-> n1
    n1 -. "3. Input to" .-> n3["Gemini API (Async)"]
    n2 -. "1. Call" .-> n4
    n4 -. "2. Get Current Mood" .-> n1
    n3 -. "4. Update Current Mood" .-> n4
    n3 -. "5. Return" .-> n5(["Result"])
    E@{ shape: rounded}
    n1@{ shape: rounded}
    n4@{ shape: rounded}
    n2@{ shape: hex}

```

### UserData
#### 儲存資料結構
```json
{
  "name": str,
  "current_mood_score": float(min=-100, max=100),
  "description": str(不超過 500 字，從使用者的歷史筆記去簡要紀錄),
  "notes": [
    {
      "date": str(紀錄筆記的日期),
      "text": str(紀錄的內容),
      "mood_score": float(min=-100, max=100)
    },
    ...
  ]

}
```

### 後端的各種 API
