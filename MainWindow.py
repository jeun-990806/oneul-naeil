from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt

from components.frames.MainFrame import MainFrame
from Controllers import DataController

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self._mainFrame = MainFrame()
        self._mainFrame.setObjectName('mainwindow')
        self._mainFrame.setStyleSheet('#mainwindow { border: 1px solid #8C8C8C; background-color: white; } QComboBox::down-arrow { image: none; } QComboBox::drop-down:button { width: 0px; border: none; }')
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.resize(400, 240)
        self.setFocus(True)
        self.setCentralWidget(self._mainFrame)
    
    def keyPressEvent(self, event) -> None:
        if event.key() == Qt.Key.Key_A:
            DataController().addTask(DataController().getTargetTasklists()[0]['id'])