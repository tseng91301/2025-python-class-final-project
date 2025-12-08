import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMenu
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer, QUrl
from PyQt5.QtMultimedia import QSoundEffect

from diary import DiaryWindow
from conversation import ConversationWindow


# ================================
#    Character 資料管理
# ================================
class Character:
    def __init__(self, name):
        self.name = name
        base = f"{name}/pic"
        sound = f"{name}/sound"

        self.rest_frames = [
            f"{base}/rest1.png",
            f"{base}/rest2.png",
        ]

        self.walk_left_frames = [
            f"{base}/walkl1.png",
            f"{base}/walkl2.png",
        ]

        self.walk_right_frames = [
            f"{base}/walkr1.png",
            f"{base}/walkr2.png",
        ]

        self.look_frames = [
            f"{base}/look1.png",
            f"{base}/look2.png",
        ]

        self.huh = f"{sound}/huh.wav"
        self.ura = f"{sound}/ura.wav"


# ================================
#         桌寵主體
# ================================
class DesktopPet(QWidget):
    def __init__(self):
        super().__init__()

        self.size = 300
        self.resize(self.size, self.size)

        # 顯示圖片的 QLabel
        self.label = QLabel(self)
        self.label.setAttribute(Qt.WA_TranslucentBackground)

        # 選擇角色
        self.character = Character("usagi")

        # 初始狀態
        self.state = "stay"
        self.direction = "right"
        self.previous_state = "stay"

        # 動畫設定
        self.frames = self.character.rest_frames
        self.index = 0

        # 設定透明視窗
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Window       # ⭐ 關鍵就是把 Qt.Tool 換成 Qt.Window
        )
        self.setAttribute(Qt.WA_TranslucentBackground)

        # 播初始圖片
        pix = self.load_pix(self.frames[self.index])
        self.label.setPixmap(pix)

        # 放在右下角
        self.move_to_bottom_right()

        # 定時器：更新動畫
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_pet)
        self.timer.start(300)

        # 音效冷卻
        self.last_sound_time = 0

        self.show()


    # ================================
    #       圖片讀取
    # ================================
    def load_pix(self, path):
        pix = QPixmap(path)
        return pix.scaled(self.size, self.size, Qt.KeepAspectRatio, Qt.SmoothTransformation)


    # ================================
    #       主動畫更新
    # ================================
    def update_pet(self):
        # LOOK 狀態不移動
        if self.state == "look":
            pass

        # 走路模式：移動
        elif self.state == "walk":
            x = self.x()
            y = self.y()
            screen = QApplication.primaryScreen().availableGeometry()
            screen_width = screen.width()

            speed = 20

            if self.direction == "right":
                x += speed
                if x + self.size >= screen_width:
                    self.direction = "left"
                    self.frames = self.character.walk_left_frames
                    self.index = 0
            else:
                x -= speed
                if x <= 0:
                    self.direction = "right"
                    self.frames = self.character.walk_right_frames
                    self.index = 0

            self.move(x, y)

        # 更新動畫幀
        self.index = (self.index + 1) % len(self.frames)
        pix = self.load_pix(self.frames[self.index])
        self.label.setPixmap(pix)


    # ================================
    #      右下角定位
    # ================================
    def move_to_bottom_right(self):
        screen = QApplication.primaryScreen().availableGeometry()
        x = screen.width() - self.size - 20
        y = screen.height() - self.size + 15
        self.move(x, y)


    # ================================
    #     右鍵選單
    # ================================
    def contextMenuEvent(self, event):
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: #fff5fa;      /* 淡粉色背景 */
                border: 2px solid #ffb7d5;      /* 粉色邊框 */
                border-radius: 10px;            /* 圓角 */
                padding: 5px;                   /* 內距 */
            }
            QMenu::item {
                font-size: 18px;                /* 字體變大 */
                padding: 10px 35px;             /* 每個選項的高度與寬度 */
                color: #444444;                 /* 文字顏色 */
                background-color: transparent;
            }
            QMenu::item:selected {
                background-color: #ffd6e7;      /* hover 粉色 */
                border-radius: 8px;             /* hover 圓角 */
            }
        """)
        diary_action = menu.addAction("日記")
        conversation_action = menu.addAction("對話")
        walk_action = menu.addAction("走走")
        stay_action = menu.addAction("乖乖待好")

        action = menu.exec_(self.mapToGlobal(event.pos()))

        if action == diary_action:
            self.previous_state = self.state
            self.state = "look"
            self.frames = self.character.look_frames
            self.index = 0
            self.open_diary()

        if action == conversation_action:
            self.previous_state = self.state
            self.state = "look"
            self.frames = self.character.look_frames
            self.index = 0
            self.open_conversation()

        elif action == walk_action and self.state != "walk":
            self.state = "walk"
            self.frames = self.character.walk_right_frames
            self.direction = "right"
            self.index = 0

        elif action == stay_action and self.state != "stay":
            self.state = "stay"
            self.frames = self.character.rest_frames
            self.move_to_bottom_right()
            self.index = 0

    # ================================
    #       開啟聊天
    # ================================
    def open_conversation(self):
        self.conversation_window = ConversationWindow()

        # 當視窗關閉 → 恢復狀態
        self.conversation_window.on_close_callback = self.restore_state

        self.conversation_window.show()

        # 桌寵移到視窗左側
        geo = self.conversation_window.geometry()
        pet_x = geo.x() - self.size - 20
        pet_y = geo.y() + geo.height() - self.size+15
        self.move(pet_x, pet_y)

    # ================================
    #       開啟日記
    # ================================
    def open_diary(self):
        self.diary_window = DiaryWindow()

        # 當視窗關閉 → 恢復狀態
        self.diary_window.on_close_callback = self.restore_state

        self.diary_window.show()

        # 桌寵移到視窗左側
        geo = self.diary_window.geometry()
        pet_x = geo.x() - self.size - 20
        pet_y = geo.y() + geo.height() - self.size+15
        self.move(pet_x, pet_y)


    # ================================
    #     恢復走路/休息狀態
    # ================================
    def restore_state(self):
        self.state = self.previous_state
        self.index = 0

        if self.state == "stay":
            self.frames = self.character.rest_frames

        elif self.state == "walk":
            if self.direction == "right":
                self.frames = self.character.walk_right_frames
            else:
                self.frames = self.character.walk_left_frames
        # ⭐ 強制立即更新一次圖片，避免卡在 look 圖片
        pix = self.load_pix(self.frames[self.index])
        self.label.setPixmap(pix)

    # ================================
    #     左鍵點擊播放音效
    # ================================
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            sound = QSoundEffect()

            if self.state == "stay":
                sound.setSource(QUrl.fromLocalFile(self.character.huh))
            else:
                sound.setSource(QUrl.fromLocalFile(self.character.ura))

            sound.setVolume(0.5)
            sound.play()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    pet = DesktopPet()
    sys.exit(app.exec_())
