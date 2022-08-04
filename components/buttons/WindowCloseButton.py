from PyQt5.QtWidgets import QWidget
from components.buttons.IconButton import IconButton

class WindowCloseButton(IconButton):
    def __init__(self, target:QWidget=None, image='assets/images/close.png', width=20, height=20):
        super().__init__(image=image, width=width, height=height)
        self._target = target

    def mousePressEvent(self, event):
        self._target.close()

    def setTarget(self, target:QWidget):
        self._target = target