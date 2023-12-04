import sys
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPainter, QPen, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow
from pynput.keyboard import Listener, KeyCode
import Files.screen_coords as screen_coords
import threaded_main as tm
import Files.interface as interface
import pyautogui

class OverlayApp:
    def __init__(self, screen_scaling=1, opacity=1):
        self.app = QApplication(sys.argv)
        self.screen_scaling = screen_scaling
        self.opacity = opacity
        self.custom_window = CustomWindow(self.app, self.screen_scaling, self.opacity)

    def run(self):
        self.custom_window.showFullScreen()
        self.custom_window.setWindowFlags(self.custom_window.windowFlags() | Qt.WindowStaysOnTopHint)
        self.custom_window.activateWindow()
        self.custom_window.raise_()
      
        print("Running OverlayApp...")
        sys.exit(self.app.exec_())

    def close_window(self):
        self.custom_window.close_window()
        self.app.quit()

class CustomWindow(QMainWindow):
    keyPressed = pyqtSignal(KeyCode)
    update_signal = pyqtSignal(list)

    def __init__(self, app, screen_scaling, opacity, parent=None):
        super().__init__(parent)
        self.update_signal.connect(self.update_overlay)
        self.listener = Listener(on_release=self.on_release)
        self.app = app
        self.screen_scaling = screen_scaling
        self.opacity = opacity
        self.target_champs = []
        self.curr_shop = []
        self.shouldDraw = False
        self.string_list = []  # Initialize an empty list to store strings
        self.draw_new_textbox = False

        # Set window flags and attributes for transparency
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WA_NoSystemBackground, True)

        self.listener.start()

        # Test call to update_overlay with static data
        self.update_overlay(["Test String 1", "Test String 2"])

    def update_overlay(self, string_list):
        print("update_overlay called with:", string_list)  # Debug print
        self.string_list = string_list
        self.draw_new_textbox = True
        self.update()

    def on_release(self, key):
        if hasattr(key, 'char') and key.char == 'd':
            self.shouldDraw = True
            self.update()

    def close_window(self):
        self.listener.stop()
        self.close()

    def paintEvent(self, event=None):
        if not self.shouldDraw and not self.draw_new_textbox:
            return

        self.curr_shop = tm.getShop()
        self.target_chaps = interface.get_curr_list()

        painter = QPainter(self)
        painter.setOpacity(self.opacity)
        self.highlight(painter)

        if self.draw_new_textbox:
            self.drawNewTextBox(painter, self.string_list)
            self.draw_new_textbox = False

    def highlight(self, painter):
        painter.setPen(QPen(Qt.red, 5, Qt.SolidLine))
        for idx, champ in enumerate(self.curr_shop):
            if champ in self.target_champs:
                self.drawHighlightRectangle(painter, idx)

    def drawHighlightRectangle(self, painter, idx):
        spacing = round(screen_coords.CHAMP_SPACING * self.screen_scaling)
        x = round(screen_coords.CHAMP_LEFT * self.screen_scaling)
        y = round(screen_coords.CHAMP_TOP * self.screen_scaling)
        height = round((screen_coords.CHAMP_BOT - screen_coords.CHAMP_TOP) * self.screen_scaling)
        width = round((screen_coords.CHAMP_RIGHT - screen_coords.CHAMP_LEFT) * self.screen_scaling)
        painter.drawRect(x + (spacing * idx), y, width, height)

    def drawNewTextBox(self, painter, string_list):
        textbox_x, textbox_y = 10, 10
        textbox_width, textbox_height = 200, 100

        painter.setOpacity(1.0)  # Ensure full opacity for the textbox
        painter.setBrush(Qt.black)
        painter.setPen(QPen(Qt.white))
        painter.drawRect(textbox_x, textbox_y, textbox_width, textbox_height)

        font = QFont()
        font.setPointSize(10)
        painter.setFont(font)

        text_y_offset = 20
        for i, text in enumerate(string_list):
            painter.drawText(textbox_x + 10, textbox_y + text_y_offset + (i * 20), text)

if __name__ == "__main__":
    overlay_app = OverlayApp(screen_scaling=1, opacity=0.8)
    overlay_app.run()
