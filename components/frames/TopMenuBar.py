from PyQt5.QtWidgets import QFrame, QGridLayout, QHBoxLayout, QWidget
from PyQt5.QtCore import Qt

from components.buttons.WindowCloseButton import WindowCloseButton
from components.buttons.LoadButton import LoadButton
from components.buttons.SaveButton import SaveButton
from components.buttons.WindowDragButton import WindowDragButton

class TopMenuBar(QFrame):
    def __init__(self, height=30):
        super().__init__()
        self.setFrameShape(QFrame.Box)
        self.setLineWidth(0)
        self.setFixedHeight(height)
        self._initWidgets()

    def _initWidgets(self):
        layout = QGridLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(5, 5, 5, 5)
        leftSide = self._initLeftSide()
        rightSide = self._initRightSide()
        
        layout.addLayout(leftSide, 0, 0, Qt.AlignmentFlag.AlignLeft)
        layout.addLayout(rightSide, 0, 1, Qt.AlignmentFlag.AlignRight)

        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 1)

    def _initLeftSide(self) -> QHBoxLayout:
        self._leftSideWidgets = [
            WindowCloseButton(),
            SaveButton(),
            LoadButton()
        ]
        leftSideBox = QHBoxLayout()
        
        for widget in self._leftSideWidgets:
            leftSideBox.addWidget(widget)

        return leftSideBox

    def _initRightSide(self) -> QHBoxLayout:
        self._rightSideWidgets = [
            WindowDragButton()
        ]
        rightSideBox = QHBoxLayout()
        
        for widget in self._rightSideWidgets:
            rightSideBox.addWidget(widget)

        return rightSideBox

    def setTargetFrame(self, target:QWidget) -> None:
        for widget in self._leftSideWidgets + self._rightSideWidgets:
            try:
                widget.setTarget(target)
            except:
                pass