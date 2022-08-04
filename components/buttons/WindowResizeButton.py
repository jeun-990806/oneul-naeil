from PyQt5.QtCore import QPoint
from components.buttons.IconButton import IconButton

class WindowResizeButton(IconButton):
    def __init__(self, target=None, image='assets/images/resizer.png', width=20, height=20, initPos=QPoint(800, 600)):
        super().__init__(image=image, width=width, height=height)
        self._target = target
        self._oldPos = initPos

    def mousePressEvent(self, event):
        self._oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self._oldPos)
        self._target.resize(self._target.width() + delta.x(), self._target.height() + delta.y())
        self._oldPos = event.globalPos()
    
    def setTarget(self, target):
        self._target = target