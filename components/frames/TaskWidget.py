from PyQt5.QtWidgets import QGridLayout, QHBoxLayout, QLabel, QComboBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from components.checkboxes.ImageCheckbox import ImageCheckbox
from components.labels.EditableLabel import EditableLabel
from components.buttons.IconButton import IconButton
from Controllers import DataController

class TaskWidget(QGridLayout):
    class TaskDeleteButton(IconButton):
        def __init__(self, target):
            super().__init__('assets/images/delete.png', width=25, height=25)
            self._target = target
        
        def mousePressEvent(self, event):
            self._target.delete()

    class TasklistSelectButton(QComboBox):
        def __init__(self, currentTasklist, target):
            super().__init__()
            self._target = target
            self._tasklists = [(tasklist['title'], tasklist['id']) for tasklist in DataController().getTargetTasklists()]
            self.setStyleSheet('color: gray; border: none; background-color: white; padding: 1px;')
            self.setFont(QFont('돋움', 7))
            self.addItems([tasklist[0] for tasklist in self._tasklists])
            self.setCurrentText(currentTasklist)

        def getCurrentTasklist(self):
            return self._tasklists[self.currentIndex()]


    def __init__(self, taskJson):
        super().__init__()
        self._task = taskJson
        self._tasklist = DataController().getTasklist(taskJson['id'])
        self._setStyle()
        self._setWidgets()

    def _setStyle(self):
        self.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        self.setContentsMargins(0, 5, 5, 5)
        self.setHorizontalSpacing(10)
    
    def _setWidgets(self):
        self._checkbox = ImageCheckbox('assets/images/checked.png', 'assets/images/unchecked.png', self._task['status'])
        self._checkbox.setFixedWidth(30)
        self._checkbox.setFixedHeight(15)
        self._checkbox.toggled.connect(self._changePlanStatus)

        metadata = QLabel('from Google Task, [')
        metadata.setStyleSheet('color: gray;')
        metadata.setFont(QFont('돋움', 7))
        metadata_r = QLabel('] ')
        metadata_r.setStyleSheet('color: gray;')
        metadata_r.setFont(QFont('돋움', 7))

        self._tasklistLabel = self.TasklistSelectButton(self._tasklist['title'], self)
        self._tasklistLabel.currentIndexChanged.connect(self._changeTasklist)
        
        self.editableLabel = EditableLabel(False)
        if self._task['status'] is 'completed':
            self.editableLabel.updateStyleSheet({'text-decoration': 'line-through'})
        else:
            self.editableLabel.updateStyleSheet({'text-decoration': 'none'})
        self.editableLabel.setText(self._task['title'])
        self.editableLabel.editingFinished.connect(self._changePlanTitle)
        
        newLayout = QGridLayout()
        metadataLayout = QHBoxLayout()
        metadataLayout.addWidget(metadata)
        metadataLayout.addWidget(self._tasklistLabel)
        metadataLayout.addWidget(metadata_r)
        if 'due' in self._task.keys():
            metadataLayout.addWidget(IconButton(image='assets/images/time_limit.png', width=9, height=9))
        metadataLayout.addStretch(1)
        newLayout.addLayout(metadataLayout, 0, 0, Qt.AlignmentFlag.AlignLeft)
        newLayout.addWidget(self.editableLabel, 1, 0)

        self.addWidget(self._checkbox, 0, 0)
        self.addLayout(newLayout, 0, 1)
        self.deleteButton = self.TaskDeleteButton(self)
        self.addWidget(self.deleteButton, 0, 2)

    def _changePlanStatus(self):
        if self._task['status'] == 'completed':
            self._task['status'] = 'needsAction'
            self.editableLabel.updateStyleSheet({'text-decoration': 'none'})
        else:
            self._task['status'] = 'completed'
            self.editableLabel.updateStyleSheet({'text-decoration': 'line-through'})
        DataController().updateTask(self._tasklist['id'], self._task)

    def _changePlanTitle(self):
        self._task['title'] = self.editableLabel.text()
        DataController().updateTask(self._tasklist['id'], self._task)

    def delete(self):
        DataController().deleteTask(self._tasklist['id'], self._task)
        self.deleteItemsOfLayout(self)
        self.setParent(None)
        self.deleteLater()
    
    def deleteItemsOfLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                else:
                    self.deleteItemsOfLayout(item.layout())

    def _changeTasklist(self):
        for tasklist in DataController().getTargetTasklists():
            if tasklist == self._tasklistLabel.getCurrentTasklist()[1]:
                self._tasklist = tasklist
                break
        DataController().moveTask(self._tasklist['id'], self._tasklistLabel.getCurrentTasklist()[1], self._task)