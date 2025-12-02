from pathlib import Path
from datetime import datetime
import json
from ..logs import Logs

class Notes:
    def __init__(self, path: Path, name: str, log_in: Logs):
        self.name = name
        self.logs = log_in
        path.mkdir(parents=True, exist_ok=True)

        self.json_file = path / f"notes_{name}.json"
        self.notes = []

        # 初始化 JSON 檔
        if not self.json_file.exists():
            with open(self.json_file, "w") as f:
                self.logs.write(f"[INIT] Log file created at {datetime.now()}")
                f.write("[]")

        # 載入資料
        with open(self.json_file, "r") as f:
            data = json.load(f)
            for item in data:
                item["datetime"] = datetime.fromisoformat(item["datetime"])
            self.notes = data

    def write(self, message: str):
        """寫入訊息並更新 notes 陣列"""
        now = datetime.now()

        new_note = {
            "note": message,
            "datetime": now,
        }
        self.notes.append(new_note)

        # 寫入 log
        self.logs.write(f"[{now}] {message}")

    def save_notes(self):
        """將 notes 儲存成 JSON"""
        serializable_notes = [
            {"note": n["note"], "datetime": n["datetime"].isoformat()}
            for n in self.notes
        ]

        with open(self.json_file, "w") as f:
            json.dump(serializable_notes, f, indent=4, ensure_ascii=False)