import sys
import Files.screen_coords as screen_coords
import threaded_main as tm
import Files.interface as interface
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from pynput.keyboard import Key, Listener, KeyCode
import pyautogui


global opc
opc = 1
global flag
flag = False

class CustomWindow(QMainWindow):
    keyPressed = pyqtSignal(KeyCode)
    
    def __init__(self, app, sc, parent=None):
        super().__init__(parent)
        self.listener = Listener(on_release=self.on_release)
        self.app = app
        self.sc = sc
        self.target_champs = []
        self.curr_shop = []
        self.shouldDraw = False

    def on_release(self, key):
        try: 
            self.keyPressed.emit(key)
        except:
            return
        
        if key.char == 'd':
            # Champ Checking Occurs Here
            self.shouldDraw = True
            self.update()

    def stop_monitoring(self):
        self.listener.stop()

    def start_monitoring(self):
        self.listener.start()

    # def updateOverlay(self):
    #     self.update()
    #     print("Ive updated!")
    #     return

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

def main(sc):
    app = QApplication(sys.argv)
    # Create the main window
    window = CustomWindow(app, sc)
    window.setWindowFlags(Qt.FramelessWindowHint)
    window.setAttribute(Qt.WA_NoSystemBackground, True)
    window.setAttribute(Qt.WA_TranslucentBackground, True)
    
    window.start_monitoring()
    # Run the application
    window.showFullScreen()
    
    # Enable Always On Top from Power Toys

    pyautogui.keyDown("ctrl")
    pyautogui.keyDown("winleft")
    pyautogui.press("t")
    pyautogui.keyUp("ctrl")
    pyautogui.keyUp("winleft")

if __name__ == "__main__":
    main(1)
