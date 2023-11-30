import sys
import pyautogui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from pynput.keyboard import Listener, KeyCode
import Files.screen_coords as screen_coords
import threaded_main as tm
import Files.interface as interface

class OverlayApp:
    def __init__(self, screen_scaling=1):
        self.app = QApplication(sys.argv)
        self.screen_scaling = screen_scaling
        self.custom_window = CustomWindow(self.app, self.screen_scaling)

    def run(self):
        self.custom_window.showFullScreen()
        self.enable_always_on_top()
        print("Running OverlayApp...")
        # sys.exit(self.app.exec_())

    def enable_always_on_top(self):
        pyautogui.keyDown("ctrl")
        pyautogui.keyDown("winleft")
        pyautogui.press("t")
        pyautogui.keyUp("ctrl")
        pyautogui.keyUp("winleft")

    def close_window(self):
        for widget in self.app.topLevelWidgets():
            if isinstance(widget, CustomWindow):
                widget.close_window()
        self.app.quit()
        

class CustomWindow(QMainWindow):
    keyPressed = pyqtSignal(KeyCode)

    def __init__(self, app, screen_scaling, parent=None):
        super().__init__(parent)
        self.listener = Listener(on_release=self.on_release)
        self.app = app
        self.screen_scaling = screen_scaling
        self.target_champs = []
        self.curr_shop = []
        self.shouldDraw = False
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.start_monitoring()

    def on_release(self, key):
        try:
            if key.char == 'd':
                self.shouldDraw = True
                self.update()
        except AttributeError:
            return

    def start_monitoring(self):
        self.listener.start()

    def stop_monitoring(self):
        self.listener.stop()

    def close_window(self):
        self.stop_monitoring()
        self.close()

    def paintEvent(self, event=None):
        if self.shouldDraw == False:
            return
        # Window painter
        self.curr_shop = tm.getShop()
        self.target_champs = interface.get_curr_list()
        print("current_shop: ", self.curr_shop)
        print("target_champs: ", self.target_champs)

        painter = QPainter(self)
        painter.setOpacity(0)
        painter.setBrush(Qt.white)
        painter.setPen(QPen(Qt.white))   
        painter.drawRect(self.rect())
        
        # Box painter
        painter1 = QPainter(self)
        painter1.setOpacity(opc)
        painter1.setPen(QPen(Qt.red,  5, Qt.SolidLine))

        for idx, champ in enumerate(self.curr_shop):
            if champ in self.target_champs:
                spacing = round(screen_coords.CHAMP_SPACING * self.sc)
                x = round(screen_coords.CHAMP_LEFT * self.sc)
                y = round(screen_coords.CHAMP_TOP * self.sc)
                height = round((screen_coords.CHAMP_BOT * self.sc) - (screen_coords.CHAMP_TOP * self.sc))
                width = round((screen_coords.CHAMP_RIGHT * self.sc) - (screen_coords.CHAMP_LEFT * self.sc))
                painter1.drawRect(x + (spacing * idx), y, width, height)
