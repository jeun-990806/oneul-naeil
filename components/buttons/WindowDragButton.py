from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QPoint
from components.buttons.IconButton import IconButton

class WindowDragButton(IconButton):
    def __init__(self, target:QWidget=None, image='assets/images/dragger.png', width=20, height=20, initPos=QPoint(800, 600)):
        super().__init__(image=image, width=width, height=height)
        self._target = target
        self._oldPos = initPos

    def setPosition(self, pos):
        self._target.move(pos)
        self._oldPos = pos

    def mousePressEvent(self, event):
        self._oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self._oldPos)
        self._target.move(self._target.x() + delta.x(), self._target.y() + delta.y())
        self._oldPos = event.globalPos()

    def setTarget(self, target:QWidget):
        self._target = target