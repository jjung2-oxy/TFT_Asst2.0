import sys
from PyQt5.QtWidgets import QApplication, QMainWindow

class CustomWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test Window")
        self.setGeometry(100, 100, 600, 400)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = CustomWindow()
    mainWin.show()
    sys.exit(app.exec_())
