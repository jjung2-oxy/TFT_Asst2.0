import sys
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPainter, QPen, QFont, QFontMetrics
from PyQt5.QtWidgets import QApplication, QMainWindow
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

        ''' CURRENT ISSUE '''
        sys.exit(self.app.exec_())

    def close_window(self):
        self.custom_window.close_window()
        self.app.quit()

class CustomWindow(QMainWindow):
    update_signal = pyqtSignal(dict)
    update2 = pyqtSignal(list)

    def __init__(self, app, screen_scaling, opacity, parent=None):
        super().__init__(parent)
        self.update_signal.connect(self.update_overlay)
        self.update2.connect(self.update_overlay2)
        self.app = app
        self.screen_scaling = screen_scaling
        self.opacity = opacity
        self.target_champs = []
        self.curr_shop = []
        self.champPool = {
            '1_cost': 29,
            '2_cost': 22,
            '3_cost': 18,
            '4_cost': 12
            # Add more if needed
        }
        self.string_dict = {}
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WA_NoSystemBackground, True)

    def setTargetChamps(self):
        self.target_champs = interface.get_curr_list()

    def update_overlay(self, stat_dict):
        self.string_dict = stat_dict  # Update the data for the textbox
        self.update()  # Trigger a repaint
        
    def update_overlay2(self, curr_shop):
        self.curr_shop = curr_shop   # Update the data for the textbox
        self.update()  # Trigger a repaint

    def close_window(self):
        self.close()

    def paintEvent(self, event=None):
        try: 
            painter = QPainter(self)
            painter.setOpacity(self.opacity)
            self.setTargetChamps()
            self.highlight(painter)
            self.drawNewTextBox(painter, self.string_dict)  # Use the updated data
        except Exception as e:
            print(f"Error in paintEvent: {e}", file=sys.stderr)

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

    def drawNewTextBox(self, painter, stats_dict):
        textbox_x, textbox_y = 10, 10
        text_y_offset = 20
        y = textbox_y + text_y_offset

        # Set the font for the text
        font = QFont()
        font.setPointSize(10)
        painter.setFont(font)

        # Use QFontMetrics to calculate text width
        font_metrics = QFontMetrics(font)
        max_text_width = 0

        # Calculate the required height and maximum width of the textbox
        textbox_height = text_y_offset  # Start with the offset as initial height
        for cost, champs in stats_dict.items():
            line = f"Top champions for cost {cost}:"
            max_text_width = max(max_text_width, font_metrics.width(line))
            textbox_height += text_y_offset  # Add space for the cost header
            for name, count in champs:
                remaining_champs = self.champPool[f'{cost}_cost'] - count
                line = f"  {name} - {count} tallied, {remaining_champs} remaining"
                max_text_width = max(max_text_width, font_metrics.width(line))
                textbox_height += text_y_offset  # Add space for each champion

        # Adjust the width of the textbox
        textbox_width = max_text_width + 20  # Add some padding

        # Draw the textbox
        painter.setOpacity(1.0)  # Ensure full opacity for the textbox
        painter.setBrush(Qt.black)
        painter.setPen(QPen(Qt.white))
        painter.drawRect(textbox_x, textbox_y, textbox_width, textbox_height)

        # Draw the text inside the textbox
        y = textbox_y + text_y_offset
        for cost, champs in stats_dict.items():
            painter.drawText(textbox_x + 10, y, f"Top champions for cost {cost}:")
            y += text_y_offset
            for name, count in champs:
                remaining_champs = self.champPool[f'{cost}_cost'] - count
                painter.drawText(textbox_x + 10, y, f"  {name} - {count} tallied, {remaining_champs} remaining")
                y += text_y_offset


if __name__ == "__main__":
    overlay_app = OverlayApp(screen_scaling=1, opacity=0.8)
    overlay_app.run()
