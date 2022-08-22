from PyQt5.QtWidgets import QLineEdit

class EditableLabel(QLineEdit):
    def __init__(self, initEditable):
        super().__init__()
        self.setFixedHeight(20)
        self.editingFinished.connect(self.handleEditingFinished)
        self._init = initEditable
        self._style = {
            'font-size': '12px',
            'border': '1px solid black',
            'text-decoration': 'none'
        }
        self._editing = False

    def showEvent(self, event):
        if self._init:
            self.edit()
            self._init = False
        else:
            self.handleEditingFinished()

    def mouseDoubleClickEvent(self, event):
        self.edit()
    
    def focusInEvent(self, event):
        if not self._editing:
            self.deselect()

    def focusOutEvent(self, event):
        if self._editing:
            self.handleEditingFinished()

    def edit(self):
        self._editing = True
        self.updateStyleSheet({'border': '1px solid black'})
        self.setFocus(True)
        self.selectAll()
        self.setReadOnly(False)

    def handleEditingFinished(self):
        self._editing = False
        self.setFocus(False)
        self.deselect()
        self.setReadOnly(True)
        self.updateStyleSheet({'border': 'none'})

    def updateStyleSheet(self, newStyleDict):
        self._style.update(newStyleDict)
        
        styleSheet = ''
        for property, value in self._style.items():
            styleSheet += property + ': ' + value + '; '
        self.setStyleSheet(styleSheet)