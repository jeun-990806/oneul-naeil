from PyQt5.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

from components.buttons.IconButton import IconButton
from components.frames.TaskWidget import TaskWidget

from Controllers import DataController

import datetime

class TaskWidgetList(QFrame):
    class TasklistPannel(QHBoxLayout):
        def __init__(self, tasklistTitle):
            super().__init__()
            self._title = tasklistTitle
        
        def reset(self):
            while self.count():
                item = self.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
            titleLabel = QLabel(self._title)
            titleLabel.setStyleSheet('font-size: 12px; font-weight: bold;')
            addButton = IconButton('assets/images/add.png')
            self.addWidget(titleLabel, alignment=Qt.AlignmentFlag.AlignLeft)
            self.addWidget(addButton, alignment=Qt.AlignmentFlag.AlignRight)
    
    def __init__(self, tasklistTitle, type):
        super().__init__()
        self.setFrameShape(QFrame.Box)
        self.setLineWidth(1)
        self.setObjectName('tasklist')
        self.setStyleSheet('#tasklist { border-top: 1px dashed gray; } ')

        DataController().attach(self)
        self._type = type

        self._layout = QVBoxLayout(self)
        self._layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self._tasklistPannel = self.TasklistPannel(tasklistTitle)

        self.updateState()

    def updateState(self):
        self.deleteItemsOfLayout(self._layout)
        self._layout.addLayout(self._tasklistPannel)
        for task in DataController().getAllTasklistItems():
            if (self._type == 'dueDate' and 'due' in task.keys() and datetime.datetime.strptime(task['due'], '%Y-%m-%dT%H:%M:%S.%fZ') < datetime.datetime.now() + datetime.timedelta(days=7)) or (self._type == 'noDueDate' and 'due' not in task.keys()):
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
        self._tasklistPannel.reset()
    
