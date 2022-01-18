from PyQt5.QtWidgets import QWidget, QLineEdit, QLabel, QMenu, QGridLayout, QVBoxLayout, QFrame
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPixmap, QIcon
import playsound


class DraggableWidget(QWidget):
    def __init__(self, initPos=QPoint(800, 600)):
        super().__init__()
        self._oldPos = initPos

    def setPosition(self, pos):
        self.move(pos)
        self._oldPos = pos

    def mousePressEvent(self, event):
        self.setFocus()
        self._oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self._oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self._oldPos = event.globalPos()

class EditableLabel(QLineEdit):
    def __init__(self, parent, initEditable):
        super().__init__()
        self.setFixedHeight(20)
        self.editingFinished.connect(self.handleEditingFinished)
        self._init = initEditable
        self._checked = False
        self._editing = False
        self._parent = parent

    def showEvent(self, event):
        if self._init:
            self.edit()
            self._init = False
        else:
            self.handleEditingFinished()

    def mouseDoubleClickEvent(self, event):
        self.edit()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            self._parent.remove()
    
    def focusInEvent(self, event):
        if not self._editing:
            self.deselect()

    def focusOutEvent(self, event):
        if self._editing:
            self.handleEditingFinished()

    def edit(self):
        self._editing = True
        self.updateStyleSheet()
        self.setFocus(True)
        self.selectAll()
        self.setReadOnly(False)

    def handleEditingFinished(self):
        self._editing = False
        self.setFocus(False)
        self.deselect()
        self.setReadOnly(True)
        self.updateStyleSheet()
        self._parent.rename(self.text())

    def check(self):
        self._checked = True
        self.updateStyleSheet()

    def uncheck(self):
        self._checked = False
        self.updateStyleSheet()

    def updateStyleSheet(self):
        styleSheet = ''
        if self._checked:
            styleSheet += 'text-decoration: line-through;'
        else:
            styleSheet += 'text-decoration: none;'
        if self._editing:
            styleSheet += 'border: 1px solid black;'
        else:
            styleSheet += 'border: none;'
        self.setStyleSheet(styleSheet)


class PlanWidget(QGridLayout):
    def __init__(self, view, plan, parent, initEditable=True):
        super().__init__()
        self._view = view
        self._data = plan
        self._parent = parent
        self._title = EditableLabel(self, initEditable)
        self._checkBox = ImageCheckbox(self, 'resources/checked.png', 'resources/unchecked.png')

        self._title.setText(plan.title)
        if self._data.checked:
            self.check()
        self.addWidget(self._checkBox, 0, 0, 1, 2)
        self.addWidget(self._title, 0, 1, 1, 8)

    def changePlanState(self):
        if self._view.changePlanState(self._data):
            self.check()
        else:
            self.uncheck()

    def check(self):
        self._checkBox.check()
        self._title.check()
        playsound.playsound('resources/check.wav', False)

    def uncheck(self):
        self._checkBox.uncheck()
        self._title.uncheck()

    def rename(self, title):
        self._view.renamePlan(self._data, title)

    def remove(self):
        self._title.deleteLater()
        self._checkBox.deleteLater()
        self.deleteLater()
        self._parent.removePlanWidget(self._data)


class ImageCheckbox(QLabel):
    def __init__(self, parent, checked, unchecked):
        super().__init__()
        self.setFixedHeight(20)
        self._parent = parent
        self._checkedImage = QPixmap(checked)
        self._uncheckedImage = QPixmap(unchecked)
        self.uncheck()

    def check(self):
        self.setPixmap(self._checkedImage)

    def uncheck(self):
        self.setPixmap(self._uncheckedImage)

    def mouseReleaseEvent(self, event):
        self._parent.changePlanState()


class MainFrame(QFrame, DraggableWidget):
    def __init__(self, view):
        super().__init__()
        self._view = view
        self._vbox = QVBoxLayout()
        self.initUI()

    def initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.resize(400, 240)
        self._vbox.setSpacing(20)
        self.setLayout(self._vbox)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_A:
            self._view.addPlan()
        elif e.key() == Qt.Key_Q:
            self.hide()

    def addPlanWidget(self, plan, initEditable=True):
        self._vbox.addLayout(PlanWidget(self._view, plan, self, initEditable=initEditable))
    
    def removePlanWidget(self, plan):
        self._view.removePlan(plan)
        self.resize(400, 240)

    def setPosition(self, pos):
        self.move(pos)


class MinimizedFrame(DraggableWidget):
    def __init__(self, view, mainWindow):
        super().__init__()
        self._view = view
        self._mainWindow = mainWindow
        self._icon = QPixmap('resources/icon.png')
        self._contextMenu = QMenu(self)
        self._saveNotionAction = None
        self._saveLocalAction = None
        self._quitAction = None
        self.initUI()

    def initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowIcon(QIcon('resources/icon.png'))
        self.resize(50, 50)

        self._mainWindow.setObjectName('mainFrame')
        self._mainWindow.setStyleSheet('#mainFrame{ background-color: white; border: 1px solid black; }')

        bg = QLabel(self)
        bg.setPixmap(self._icon)

        self._saveLocalAction = self._contextMenu.addAction("Save to local")
        self._saveNotionAction = self._contextMenu.addAction("Save to Notion")
        self._quitAction = self._contextMenu.addAction("Quit")

        self.show()

    def mouseDoubleClickEvent(self, event):
        if self._mainWindow.isVisible():
            self._mainWindow.hide()
        else:
            self._mainWindow.show()

    def contextMenuEvent(self, event):
        action = self._contextMenu.exec_(event.globalPos())
        if action == self._saveLocalAction:
            self._view.savePlanData()
        elif action == self._saveNotionAction:
            print("save plan data to notion")
        elif action == self._quitAction:
            self._view.close()
