from PyQt5.QtWidgets import QPushButton
import playsound
from Controllers import DataController

class ImageCheckbox(QPushButton):
    def __init__(self, checked, unchecked, initStatus='needsAction'):
        super().__init__()
        self.setCheckable(True)
        self._checkedImage = checked
        self._uncheckedImage = unchecked
        self.status = initStatus
        if self.status == 'completed':
            self.setStyleSheet('border: none; background-image: url(' + self._checkedImage + '); background-repeat: no-repeat; background-position: 0 0;')
        else:
            self.setStyleSheet('border: none; background-image: url(' + self._uncheckedImage + '); background-repeat: no-repeat; background-position: 0 0;')

    def toggle(self):
        if self.status == 'completed':
            self.status = 'needsAction'
        else:
            self.status = 'completed'
        if self.status == 'completed':
            self.check()
        else:
            self.uncheck()
        return super().toggle()
    
    def mouseReleaseEvent(self, event):
        self.toggle()

    def check(self):
        self.setStyleSheet('border: none; background-image: url(' + self._checkedImage + '); background-repeat: no-repeat; background-position: 0 0;')
        playsound.playsound('assets/audio/check.wav', block=False)

    def uncheck(self):
        self.setStyleSheet('border: none; background-image: url(' + self._uncheckedImage + '); background-repeat: no-repeat; background-position: 0 0;')
