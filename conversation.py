from PyQt5.QtWidgets import (
    QWidget, QApplication, QVBoxLayout, QHBoxLayout,
    QTextEdit, QLineEdit, QPushButton
)
from PyQt5.QtCore import QTimer
import api_connect as api

class ConversationWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Conversation")
        self.resize(500, 350)

        # 移到螢幕右下角
        screen = QApplication.primaryScreen().availableGeometry()
        x = screen.width() - self.width() - 20
        y = screen.height() - self.height() - 20
        self.move(x, y)

        # --------------------------
        # UI 介面
        # --------------------------
        layout = QVBoxLayout(self)

        # 顯示區
        self.chat_box = QTextEdit()
        self.chat_box.setReadOnly(True)

        # 水平區：輸入框 + 送出按鈕
        input_layout = QHBoxLayout()
        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("發送訊息")
        self.send_button = QPushButton("送出")

        input_layout.addWidget(self.input_box)
        input_layout.addWidget(self.send_button)

        layout.addWidget(self.chat_box)
        layout.addLayout(input_layout)

        # --------------------------
        # 事件綁定
        # --------------------------
        self.send_button.clicked.connect(self.send_message)
        self.input_box.returnPressed.connect(self.send_message)

        # AI 回覆檢查
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_ai)
        self.timer.start(300)

        api.init("桌寵使用者", force=False)

        # 由 main.py 設定關閉事件 callback
        self.on_close_callback = None

    # --------------------------
    # 使用者送出訊息（日記）
    # --------------------------
    def send_message(self):
        text = self.input_box.text().strip()
        if not text:
            return

        self.chat_box.append(f"🧑：{text}")
        self.input_box.clear()

        # ⭐ AI 回覆（一次性）
        api.conversation_bg(text)

    # --------------------------
    # 檢查 AI 回覆
    # --------------------------
    def check_ai(self):
        if api.genai_waiting:
            return

        if api.genai_response:
            self.chat_box.append(f"/ᐠ .ᆺ. ᐟ\ﾉ：{api.genai_response}")
            api.genai_response = ""

    # --------------------------
    # 視窗關閉
    # --------------------------
    def closeEvent(self, event):
        if self.on_close_callback:
            self.on_close_callback()
        event.accept()
