from PyQt5.QtWidgets import QGridLayout, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from components.checkboxes.ImageCheckbox import ImageCheckbox
from components.labels.EditableLabel import EditableLabel
from components.buttons.IconButton import IconButton

class TaskWidget(QGridLayout):
    def __init__(self, title='untitled', status=False):
        super().__init__()
        self._title = title
        self._status = status
        self._setStyle()
        self._setWidgets()

    def _setStyle(self):
        self.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        self.setContentsMargins(0, 5, 5, 5)
        self.setHorizontalSpacing(10)
    
    def _setWidgets(self):
        self._checkbox = ImageCheckbox('assets/images/checked.png', 'assets/images/unchecked.png', self._status)
        self._checkbox.setFixedWidth(30)
        self._checkbox.setFixedHeight(15)
        self._checkbox.toggled.connect(self._changePlanStatus)

        metadata = QLabel('from Google Task, [To-Do] ')
        metadata.setStyleSheet('color: gray;')
        testfont = QFont('돋움', 7)
        metadata.setFont(testfont)
        
        self.editableLabel = EditableLabel(False)
        if self._status is True:
            self.editableLabel.updateStyleSheet({'text-decoration': 'line-through'})
        else:
            self.editableLabel.updateStyleSheet({'text-decoration': 'none'})
        self.editableLabel.setText(self._title)
        self.editableLabel.editingFinished.connect(self._changePlanTitle)
        
        newLayout = QGridLayout()
        metadataLayout = QHBoxLayout()
        metadataLayout.addWidget(metadata)
        metadataLayout.addWidget(IconButton(image='assets/images/time_limit.png', width=9, height=9))
        metadataLayout.addStretch(1)
        newLayout.addLayout(metadataLayout, 0, 0, Qt.AlignmentFlag.AlignLeft)
        newLayout.addWidget(self.editableLabel, 1, 0)

        self.addWidget(self._checkbox, 0, 0)
        self.addLayout(newLayout, 0, 1)
        self.addWidget(IconButton('assets/images/delete.png', width=25, height=25), 0, 2)

    def _changePlanStatus(self):
        self._status = not self._status
        if self._status:
            self.editableLabel.updateStyleSheet({'text-decoration': 'line-through'})
        else:
            self.editableLabel.updateStyleSheet({'text-decoration': 'none'})

    def _changePlanTitle(self):
        self._title = self.editableLabel.text()