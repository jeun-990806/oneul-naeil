from PyQt5.QtWidgets import QFrame, QGridLayout, QHBoxLayout
from PyQt5.QtCore import Qt

from components.buttons.WindowResizeButton import WindowResizeButton

class BottomMenuBar(QFrame):
    def __init__(self, height=30):
        super().__init__()
        self.setFrameShape(QFrame.Box)
        self.setLineWidth(1)
        self.setObjectName('bottomMenuBar')
        self.setStyleSheet('#bottomMenuBar { border-top: 1px dashed gray; }')

        self.setFixedHeight(height)
        self._setWidgets()

    def _setWidgets(self):
        layout = QGridLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignBottom)
        layout.setSpacing(0)
        layout.setContentsMargins(5, 5, 5, 5)
        leftSide = self._leftSide()
        rightSide = self._rightSide()
        
        layout.addLayout(leftSide, 0, 0, Qt.AlignmentFlag.AlignLeft)
        layout.addLayout(rightSide, 0, 1, Qt.AlignmentFlag.AlignRight)

        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 1)

    def _leftSide(self) -> QHBoxLayout:
        # Left Side Widgets
        self._leftSideWidgets = []
        leftSideBox = QHBoxLayout()
        
        for widget in self._leftSideWidgets:
            leftSideBox.addWidget(widget)

        return leftSideBox

    def _rightSide(self) -> QHBoxLayout:
        # Right Side Widgets
        self._rightSideWidgets = [
                WindowResizeButton(self.parent())
            ]
        rightSideBox = QHBoxLayout()
        
        for widget in self._rightSideWidgets:
            rightSideBox.addWidget(widget)

        return rightSideBox

    def setTargetFrame(self, target:QFrame):
        for widget in self._leftSideWidgets + self._rightSideWidgets:
            try:
                widget.setTarget(target)
            except:
                pass