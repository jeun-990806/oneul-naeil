from PyQt5.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from components.buttons.IconButton import IconButton
from components.frames.TaskWidget import TaskWidget

from Controllers import DataController

class TaskWidgetList(QFrame):
    def __init__(self, controller=None, category=''):
        super().__init__()
        self.setFrameShape(QFrame.Box)
        self.setLineWidth(0)

        self._controller = controller
        DataController().attach(self)

        categoryTitle = QHBoxLayout()
        
        self._list = QLabel(category, self)
        self._list.setFont(QFont('돋움', 7))
        self._addButton = IconButton('resources/add.png')
        categoryTitle.addWidget(self._list, alignment=Qt.AlignmentFlag.AlignLeft)
        categoryTitle.addWidget(self._addButton, alignment=Qt.AlignmentFlag.AlignRight)

        self._layout = QVBoxLayout(self)
        self._layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.updateState()

    def updateState(self):
        self.deleteItemsOfLayout(self._layout)
        for task in DataController().getAllTasklistItems():
            self._layout.addLayout(TaskWidget(task))

    def deleteItemsOfLayout(self, layout):
     if layout is not None:
         while layout.count():
             item = layout.takeAt(0)
             widget = item.widget()
             if widget is not None:
                 widget.setParent(None)
             else:
                 self.deleteItemsOfLayout(item.layout())
