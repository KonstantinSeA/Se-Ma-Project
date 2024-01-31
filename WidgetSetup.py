import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLabel, QFileDialog
from PyQt5.QtGui import QImage, QPixmap
from PyQt5 import uic

from plays import game


class StartedMenu(QWidget):
    # Виджет для Отображения Стартового Меню
    def __init__(self):
        super().__init__()
        uic.loadUi('MenuDesign/StartedMenu.ui', self)
        self.initUI()

    def initUI(self):
        self.setStyleSheet('background-color: #32393a')
        self.Main_label.setStyleSheet('color: #fffcff;')
        self.Play_button.setStyleSheet('background: #466363; color: #fffcff;')
        self.Play_button.clicked.connect(self.run_play)
        self.Save_button.setStyleSheet('background: #466363; color: #fffcff;')
        self.Save_button.clicked.connect(self.run_save)
        self.Exit_button.setStyleSheet('background: #466363; color: #fffcff;')
        self.Exit_button.clicked.connect(self.run_exit)

    def run_play(self):
        self.hide()
        game.save = 'a'
        game.init()
        game.run()
        sys.exit()

    def run_save(self):
        self.save_menu = SavesMenu(self)
        self.hide()
        self.save_menu.show()

    def run_exit(self):
        sys.exit()


class SavesMenu(QWidget):
    # Виджет для Отображения Меню Выбора Сохранений
    def __init__(self, prev):
        super().__init__()
        self.prev = prev
        uic.loadUi('MenuDesign/SavesMenu.ui', self)
        self.initUI()

    def initUI(self):
        self.setStyleSheet('background-color: #32393a')
        self.Main_label.setStyleSheet('color: #fffcff;')
        self.SaveA_button.setStyleSheet('background: #466363; color: #fffcff;')
        self.SaveA_button.clicked.connect(self.run_savea)
        self.SaveB_button.setStyleSheet('background: #466363; color: #fffcff;')
        self.SaveB_button.clicked.connect(self.run_saveb)
        self.SaveC_button.setStyleSheet('background: #466363; color: #fffcff;')
        self.SaveC_button.clicked.connect(self.run_savec)
        self.SaveD_button.setStyleSheet('background: #466363; color: #fffcff;')
        self.SaveD_button.clicked.connect(self.run_saved)
        self.Exit_button.setStyleSheet('background: #466363; color: #fffcff;')
        self.Exit_button.clicked.connect(self.run_exit)

    def run_savea(self):
        self.game_menu = GameMenu(self, 'a')
        self.hide()
        self.game_menu.show()

    def run_saveb(self):
        self.game_menu = GameMenu(self, 'b')
        self.hide()
        self.game_menu.show()

    def run_savec(self):
        self.game_menu = GameMenu(self, 'c')
        self.hide()
        self.game_menu.show()

    def run_saved(self):
        self.game_menu = GameMenu(self, 'd')
        self.hide()
        self.game_menu.show()

    def run_exit(self):
        self.hide()
        self.prev.show()


class GameMenu(QWidget):
    # Виджет для Отображения Меню выбора действия с сохранением
    def __init__(self, prev, save):
        super().__init__()
        self.prev, self.save = prev, save
        uic.loadUi('MenuDesign/GameMenu.ui', self)
        self.initUI()

    def initUI(self):
        self.setStyleSheet('background-color: #32393a')
        self.Main_label.setStyleSheet('color: #fffcff;')
        self.Exit_button.setStyleSheet('background: #466363; color: #fffcff;')
        self.Exit_button.clicked.connect(self.run_exit)
        self.Play_button.setStyleSheet('background: #466363; color: #fffcff;')
        self.Play_button.clicked.connect(self.run_play)
        self.Reset_button.setStyleSheet('background: #466363; color: #fffcff;')
        self.Reset_button.clicked.connect(self.run_reset)

    def run_play(self):
        self.hide()
        game.save = self.save
        game.init()
        game.run()
        sys.exit()

    def run_reset(self):
        game.save = self.save
        game.reset()

    def run_exit(self):
        self.hide()
        self.prev.show()
