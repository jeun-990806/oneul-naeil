from PyQt5.QtWidgets import QFrame, QVBoxLayout

from components.frames.TopMenuBar import TopMenuBar
from components.frames.BottomMenuBar import BottomMenuBar
from components.frames.TaskWidgetList import TaskWidgetList

class MainFrame(QFrame):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.topMenuBar = TopMenuBar()
        self.bottomMenuBar = BottomMenuBar()
        self.taskWidgetList_A = TaskWidgetList('~7일', 'dueDate')
        self.taskWidgetList_B = TaskWidgetList('자율', 'noDueDate')

        layout = QVBoxLayout(self)
        layout.addWidget(self.topMenuBar)
        layout.addWidget(self.taskWidgetList_A)
        layout.addWidget(self.taskWidgetList_B)
        layout.addWidget(self.bottomMenuBar)

        self.topMenuBar.setTargetFrame(self)
        self.bottomMenuBar.setTargetFrame(self)

        self.resize(500, 500)
        self.show()

    def x(self):
        return self.parent().x()

    def y(self):
        return self.parent().y()

    def width(self):
        return self.parent().width()
    
    def height(self):
        return self.parent().height()

    def move(self, xPos, yPos):
        return self.parent().move(xPos, yPos)

    def resize(self, width, height):
        super().resize(width, height)
        if self.parent() is not None:
            self.parent().resize(width, height)

    def close(self):
        super().close()
        return self.parent().close()