import sys
from PyQt5.QtWidgets import QApplication

from WidgetSetup import StartedMenu

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = StartedMenu()
    ex.show()
    sys.exit(app.exec())
