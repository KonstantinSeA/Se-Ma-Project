import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt5 import uic

from MenuDesign.WidgetSetup import StartedMenu

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = StartedMenu()
    ex.show()
    sys.exit(app.exec())
