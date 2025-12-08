from PyQt5.QtWidgets import (
    QWidget, QApplication, QVBoxLayout, QHBoxLayout,
    QTextEdit, QLineEdit, QPushButton
)
import api_connect as api

from RecordWindow import RecordWindow  # ⭐ 新增：載入紀錄視窗


class DiaryWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Diary")
        self.resize(500, 150)

        # 移到螢幕右下角
        screen = QApplication.primaryScreen().availableGeometry()
        x = screen.width() - self.width() - 20
        y = screen.height() - self.height() - 20
        self.move(x, y)

        # --------------------------
        # UI 介面
        # --------------------------
        layout = QVBoxLayout(self)

        # 水平區：輸入框 + 送出按鈕
        input_layout = QHBoxLayout()
        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("寫下你的日記...")
        self.send_button = QPushButton("送出")

        input_layout.addWidget(self.input_box)
        input_layout.addWidget(self.send_button)

        # 紀錄按鈕
        self.record_button = QPushButton("紀錄")

        layout.addLayout(input_layout)
        layout.addWidget(self.record_button)

        # --------------------------
        # 事件綁定
        # --------------------------
        self.send_button.clicked.connect(self.send_message)
        self.input_box.returnPressed.connect(self.send_message)
        self.record_button.clicked.connect(self.open_record_window)

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

        # ⭐ 寫入 notes（日記）
        api.write_note(text, mood_test=True)
        
        self.input_box.clear()

    # --------------------------
    # 打開紀錄視窗
    # --------------------------
    def open_record_window(self):
        self.record_window = RecordWindow()
        self.record_window.show()

    # --------------------------
    # 視窗關閉
    # --------------------------
    def closeEvent(self, event):
        if self.on_close_callback:
            self.on_close_callback()
        event.accept()
