from PyQt5.QtCore import pyqtSlot, QObject, pyqtSignal

class ButtonSignal(QObject):
    _message:str
    _signal = pyqtSignal(str)

    def run(self):
        self._signal.emit(self._message)
    
    def setMessage(self, message:str) -> None:
        self._message = message
    
    def getMessage(self) -> str:
        return self._message