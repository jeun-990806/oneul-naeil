from PyQt5.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from components.buttons.IconButton import IconButton
from components.frames.TaskWidget import TaskWidget

class TaskWidgetList(QFrame):
    def __init__(self, parent=None, controller=None, category=''):
        super().__init__(parent)
        self.setFrameShape(QFrame.Box)
        self.setLineWidth(0)

        self._controller = controller

        categoryTitle = QHBoxLayout()
        
        self._list = QLabel(category, self)
        self._list.setFont(QFont('돋움', 7))
        self._addButton = IconButton('resources/add.png')
        categoryTitle.addWidget(self._list, alignment=Qt.AlignmentFlag.AlignLeft)
        categoryTitle.addWidget(self._addButton, alignment=Qt.AlignmentFlag.AlignRight)

        self._layout = QVBoxLayout(self)
        self._layout.addLayout(categoryTitle)
        self._layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self._loadTasks()

    def _loadTasks(self):
        TaskDataList = [
            {'title': 'test01', 'status': False},
            {'title': 'test02', 'status': True}
            ]
        for TaskData in TaskDataList:
            self.addTaskWidget(TaskData)
    
    def addTaskWidget(self, TaskData):
        TaskWidget = self._createTaskWidget(TaskData)
        self._layout.addLayout(TaskWidget)

    def _createTaskWidget(self, TaskData):
        return TaskWidget(title=TaskData['title'], status=TaskData['status'])