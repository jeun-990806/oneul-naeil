from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt

from components.frames.MainFrame import MainFrame

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self._mainFrame = MainFrame()
        self._mainFrame.setObjectName('mainwindow')
        self._mainFrame.setStyleSheet('#mainwindow { border: 1px solid #8C8C8C; background-color: white; }')
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.resize(400, 240)
        self.setCentralWidget(self._mainFrame)