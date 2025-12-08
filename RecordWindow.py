from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QListWidget, QTextEdit
)
import json
import os
import api_connect   # ⭐ 從這裡取得 userData.jsonFile


class RecordWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("日記紀錄")
        self.resize(600, 400)

        json_path = api_connect.userData.storage_path / f"{api_connect.userData.name}.json"
        print("📁 正在讀取 JSON：", json_path)

        if json_path.exists():
            with open(json_path, "r", encoding="utf-8") as f:
                self.data = json.load(f)
        else:
            print("❌ 找不到 JSON！")
            self.data = {"notes": []}

        # notes 部分
        notes = self.data.get("notes", [])

        # ⭐ 新到舊排序
        notes = sorted(notes, key=lambda n: n["dateTime"], reverse=True)
        self.notes = notes

        # --------------------------
        # UI 排版
        # --------------------------
        layout = QHBoxLayout(self)

        # 左邊：日記列表
        self.list_widget = QListWidget()
        for n in notes:
            date = n["dateTime"].split("T")[0]
            short = n["text"][:10]
            self.list_widget.addItem(f"{date}  {short}...")

        # 右邊：內容顯示框
        self.detail_box = QTextEdit()
        self.detail_box.setReadOnly(True)

        layout.addWidget(self.list_widget, 1)
        layout.addWidget(self.detail_box, 2)

        # 點選顯示內容
        self.list_widget.currentRowChanged.connect(self.display_note)

        # ⭐ 自動選第一筆
        if len(self.notes) > 0:
            self.list_widget.setCurrentRow(0)
            self.display_note(0)

    def display_note(self, index):
        if index < 0 or index >= len(self.notes):
            return

        note = self.notes[index]
        date = note["dateTime"].split("T")[0]
        text = note["text"]
        mood = note.get("mood_score", "無")

        show = (
            f"📅 日期：{date}\n\n"
            f"📝 內容：\n{text}\n\n"
            f"💖 心情值：{mood}\n"
        )

        self.detail_box.setText(show)
