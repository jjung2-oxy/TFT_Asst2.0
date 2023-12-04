import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from pynput.keyboard import Listener, KeyCode
import Files.screen_coords as screen_coords
import threaded_main as tm
import Files.interface as interface

class OverlayApp:
    def __init__(self, screen_scaling=1, opacity=1):
        self.app = QApplication(sys.argv)
        self.screen_scaling = screen_scaling
        self.opacity = opacity  # Replacing the global variable 'opc'
        self.custom_window = CustomWindow(self.app, self.screen_scaling, self.opacity)

    def run(self):
        self.custom_window.showFullScreen()
        self.enable_always_on_top()
        print("Running OverlayApp...")
        sys.exit(self.app.exec_())

    def enable_always_on_top(self):
        self.custom_window.setWindowFlags(self.custom_window.windowFlags() | Qt.WindowStaysOnTopHint)

    def close_window(self):
        for widget in self.app.topLevelWidgets():
            if isinstance(widget, CustomWindow):
                widget.close_window()
        self.app.quit()

class CustomWindow(QMainWindow):
    keyPressed = pyqtSignal(KeyCode)

    def __init__(self, app, screen_scaling, opacity, parent=None):
        super().__init__(parent)
        self.listener = Listener(on_release=self.on_release)
        self.app = app
        self.screen_scaling = screen_scaling
        self.opacity = opacity  # Using passed opacity value
        self.target_champs = []
        self.curr_shop = []
        self.shouldDraw = False
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.start_monitoring()

    def on_release(self, key):
        try:
            if key.char == 'd':
                self.shouldDraw = True
                self.update()
        except AttributeError:
            pass  # Ignore other keys without a char attribute

    def start_monitoring(self):
        self.listener.start()

    def stop_monitoring(self):
        self.listener.stop()

    def close_window(self):
        self.stop_monitoring()
        self.close()

    def paintEvent(self, event=None):
        if not self.shouldDraw:
            return
        
        self.curr_shop = tm.getShop()
        self.target_champs = interface.get_curr_list()
        print("current_shop: ", self.curr_shop)
        print("target_champs: ", self.target_champs)

        painter = QPainter(self)
        painter.setOpacity(0)  # Invisible painter for layout logic
        
        highlight_painter = QPainter(self)
        highlight_painter.setOpacity(self.opacity)
        highlight_painter.setPen(QPen(Qt.red, 5, Qt.SolidLine))
        self.highlight(highlight_painter)

    def highlight(self, painter):
        for idx, champ in enumerate(self.curr_shop):
            if champ in self.target_champs:
                spacing = round(screen_coords.CHAMP_SPACING * self.screen_scaling)
                x = round(screen_coords.CHAMP_LEFT * self.screen_scaling)
                y = round(screen_coords.CHAMP_TOP * self.screen_scaling)
                height = round((screen_coords.CHAMP_BOT - screen_coords.CHAMP_TOP) * self.screen_scaling)
                width = round((screen_coords.CHAMP_RIGHT - screen_coords.CHAMP_LEFT) * self.screen_scaling)
                painter.drawRect(x + (spacing * idx), y, width, height)

    def drawTextBox(self, painter):
        painter.setOpacity(1.0)
        painter.setBrush(Qt.black)
        painter.setPen(QPen(Qt.white))

        textbox_x = 10
        textbox_y = 10
        textbox_width = 200
        textbox_height = 100

        painter.drawRect(textbox_x, textbox_y, textbox_width, textbox_height)

        font = QFont()
        font.setPointSize(10)
        painter.setFont(font)

        text_content = "Your dynamic text here"
        painter.drawText(textbox_x + 10, textbox_y + 20, text_content)
