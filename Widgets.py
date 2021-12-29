from PyQt5.QtWidgets import QWidget, QLineEdit, QLabel, QGridLayout, QVBoxLayout
from PyQt5.QtCore import Qt, QEvent, QPoint
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
        self._oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self._oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self._oldPos = event.globalPos()


class PlanWidget(QGridLayout):
    def __init__(self, view, plan):
        super().__init__()
        self._view = view
        self._data = plan
        self._title = EditableLabel(self, self._data.title)
        self._checkBox = ImageCheckbox(self, 'resources/checked.png', 'resources/unchecked.png')
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
        self._title.rename(title)

    def remove(self):
        self._title.deleteLater()
        self._checkBox.deleteLater()
        self.deleteLater()


class ImageCheckbox(QLabel):
    def __init__(self, parent, checked, unchecked):
        super().__init__()
        self.setFixedHeight(15)
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


class EditableLabel(QLabel):
    def __init__(self, parent, title):
        super().__init__(title)
        self.setMaximumWidth(350)
        self._parent = parent
        self._initPositionSetting = 0

        self._editor = QLineEdit(self)
        self._editor.setWindowFlags(Qt.Popup)
        self._editor.setFocusProxy(self)
        self._editor.editingFinished.connect(self.handleEditingFinished)
        self._editor.installEventFilter(self)
        self.editTitle()

    def editTitle(self):
        self._editor.setText(self.text())
        self._editor.move(self.mapToGlobal(self.rect().topLeft()))
        if not self._editor.isVisible():
            self._editor.show()
            self._editor.selectAll()

    def check(self):
        self.setStyleSheet('text-decoration: line-through;')

    def uncheck(self):
        self.setStyleSheet('text-decoration: none;')

    def rename(self, title):
        self.setText(title)

    def setEditorPosition(self):
        self._editor.move(self.mapToGlobal(self.rect().topLeft()))

    def eventFilter(self, widget, event):
        if event.type() == QEvent.MouseButtonPress and not self._editor.geometry().contains(event.globalPos()):
            self._editor.hide()
            self.handleEditingFinished()
            return True
        # 아마도... 비동기적 처리 과정이 있는 것 같다.
        # 위젯 생성 -> 그리드 레이아웃 -> VBox 레이아웃 순으로 배치한 뒤, Global Position을 가져올 수 있으면 좋을 것 같은데...
        if self._initPositionSetting < 16:
            self._editor.move(self.mapToGlobal(self.rect().topLeft()))
            self._initPositionSetting += 1
        return super().eventFilter(widget, event)

    def mouseDoubleClickEvent(self, event):
        self.editTitle()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            self._parent.remove()

    def handleEditingFinished(self):
        self._parent.rename(self._editor.text())
        self._editor.hide()


class MainFrame(DraggableWidget):
    def __init__(self, view):
        super().__init__()
        self._view = view
        self._vbox = QVBoxLayout()
        self.initUI()

    def initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.resize(320, 240)
        self._vbox.setSpacing(20)
        self.setLayout(self._vbox)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_A:
            self._view.addPlan()
        elif e.key() == Qt.Key_Q:
            self.hide()

    def addPlanWidget(self, plan):
        self._vbox.addLayout(PlanWidget(self._view, plan))
        self.setLayout(self._vbox)


class MinimizedFrame(DraggableWidget):
    def __init__(self, view, mainWindow):
        super().__init__()
        self._view = view
        self._mainWindow = mainWindow
        self._icon = QPixmap('resources/icon.png')
        self.initUI()

    def initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowIcon(QIcon('resources/icon.png'))
        self.resize(50, 50)

        self._mainWindow.setObjectName('mainFrame')
        self._mainWindow.setStyleSheet('QWidget#mainFrame{ background-color: white; border: 1px solid black; }')

        bg = QLabel(self)
        bg.setPixmap(self._icon)

        self.show()

    def mouseDoubleClickEvent(self, event):
        if self._mainWindow.isVisible():
            self._mainWindow.hide()
        else:
            self._mainWindow.show()

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.button() == Qt.MouseButton.RightButton:
            self._view.close()
