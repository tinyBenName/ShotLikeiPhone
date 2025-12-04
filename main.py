import sys
import os
from PyQt5 import QtWidgets, QtCore, QtGui
import pyautogui
from datetime import datetime
from pygame import mixer
import keyboard
import threading

# ================== 闪屏窗口 ==================
class FlashWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # 全屏、无边框、置顶、工具窗口
        self.setWindowFlags(
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.Tool
        )

        # 白色背景
        self.setStyleSheet("background-color: white;")
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        self.setWindowOpacity(1.0)

        # 渐隐动画
        self.animation = QtCore.QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(1000)  # 0.5 秒
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.0)
        self.animation.finished.connect(self.on_finished)

    def showEvent(self, event):
        self.animation.start()
        super().showEvent(event)

    def on_finished(self):
        self.close()  # 只关闭闪屏窗口，不退出托盘程序

# ================== 截图函数 ==================
def screenshot_all_screens():
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    screenshot = pyautogui.screenshot()
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = os.path.join(desktop, f"screenshot_{timestamp}.png")
    screenshot.save(filename)
    print(f"截图已保存到: {filename}")

# ================== 闪屏 + 截图 ==================
def wink():
    flash = FlashWindow()
    flash.showFullScreen()  # 显示全屏窗口

def voice():
    mixer.init()
    mixer.music.load("wink.mp3")
    mixer.music.play()

def left_click():
    threading.Thread(target=screenshot_all_screens).start()
    threading.Thread(target=voice).start()
    wink()  # 创建闪屏窗口


# ================== 退出程序 ==================
def exit_app():
    tray.hide()  # 隐藏托盘图标
    sys.exit()


# ================== 主程序 ==================
app = QtWidgets.QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)  # 确保托盘程序不会因为没有窗口退出

# 创建系统托盘图标
tray = QtWidgets.QSystemTrayIcon(QtGui.QIcon("jama.ico"), app)
tray_ref = tray
tray.setToolTip("嘤嘤嘤截图")
tray.show()

# 托盘右键菜单
menu = QtWidgets.QMenu()
exit_action = menu.addAction("退出 嘤嘤嘤截图")
exit_action.triggered.connect(exit_app)
tray.setContextMenu(menu)

# 左键点击事件
def on_tray_activated(reason):
    if reason == QtWidgets.QSystemTrayIcon.Trigger:  # 左键单击
        left_click()
tray.activated.connect(on_tray_activated)



# alt+z
# 1️⃣ 定义信号类
class HotkeySignal(QtCore.QObject):
    trigger = QtCore.pyqtSignal()  # 信号不带参数

hotkey_signal = HotkeySignal()
hotkey_signal.trigger.connect(left_click)  # 主线程执行 left_click

# 2️⃣ 修改热键回调
def hotkey_action():
    print("Alt+Z 被按下")
    hotkey_signal.trigger.emit()  # 发射信号给主线程

keyboard.add_hotkey("alt+z", hotkey_action)

wink()

# 运行主事件循环
sys.exit(app.exec_())


