from os import remove
from PyQt5.QtWidgets import QMainWindow, QFrame, QGridLayout, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QGroupBox, QCheckBox
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QCursor

from googleapiclient.discovery import build

from components.buttons.WindowCloseButton import WindowCloseButton
from Controllers import SyncController, DataController

class SyncButton(QPushButton):
    def __init__(self):
        super().__init__()
        SyncController().addTargetComponents(self)
        self._render()

    def _render(self):
        if SyncController().checkAuthorization():
            self._credentials = SyncController().getCredentials()
            self._getUserInfo()
            self.setText(self._userInfo['email'] + '에 연결됨')
            self.setDisabled(True)
        else: 
            self.setText('동기화된 계정 없음')
            self.setDisabled(False)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

    def mousePressEvent(self, event) -> None:
        SyncController().authorize()

    def setCredentials(self, credentials):
        self._credentials = credentials

    def reRender(self):
        self._render()

    def setDisabled(self, value) -> None:
        if value:
            self.setStyleSheet('text-align: left; font-size: 12px; color: black; border: none; padding: 5px;')
        else:
            self.setStyleSheet('font-size: 12px; color: black; border: 1px solid black; padding: 5px')
        return super().setDisabled(value)
    
    def _getUserInfo(self):
        try:
            service = build('oauth2', 'v2', credentials=self._credentials)
            self._userInfo = service.userinfo().get().execute()
        except Exception as err:
            print(err)

class TopMenu(QFrame):
    def __init__(self, titleText, parent):
        super().__init__()
        self._parent = parent
        self._render(titleText)

    def _render(self, titleText):
        leftSide = QHBoxLayout()
        title = QLabel(titleText)
        leftSide.addWidget(title)

        rightSide = QHBoxLayout()
        closeButton = WindowCloseButton()
        closeButton.setTarget(self._parent)
        rightSide.addWidget(closeButton)

        topMenuLayout = QGridLayout()
        topMenuLayout.addLayout(leftSide, 0, 0, Qt.AlignmentFlag.AlignLeft)
        topMenuLayout.addLayout(rightSide, 0, 1, Qt.AlignmentFlag.AlignRight)
        self.setLayout(topMenuLayout)

    def mousePressEvent(self, event):
        self._oldPos = event.globalPos()
    
    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self._oldPos)
        self._parent.move(self._parent.x() + delta.x(), self._parent.y() + delta.y())
        self._oldPos = event.globalPos()
    
class SyncPannel(QGroupBox):
    def __init__(self):
        super().__init__('동기화')
        self._render()
    
    def _render(self):
        self.setStyleSheet('font-size: 12px;')
        layout = QVBoxLayout()
        syncButton = SyncButton()
        layout.addWidget(syncButton)
        self.setLayout(layout)

class Tasklist:
    def __init__(self, tasklistId, title):
        self._id = tasklistId
        self._title = title

    def getTitle(self):
        return self._title
    
    def getId(self):
        return self._id

class TasklistCheckBox(QCheckBox):
    def __init__(self, tasklist):
        super().__init__(tasklist.getTitle())
        self._tasklist = tasklist
        self.stateChanged.connect(self._toggle)
    
    def _getTasks(self):
        credentials = SyncController().getCredentials()
        service = build('tasks', 'v1', credentials=credentials)
        return service.tasks().list(tasklist=self._tasklist.getId()).execute()

    def _toggle(self):
        if self.isChecked(): DataController().addTasklist(self._tasklist.getId())
        else: DataController().removeTasklist(self._tasklist.getId())
        DataController().printTasklist()

class TasklistPannel(QGroupBox):
    def __init__(self):
        super().__init__('태스크리스트 관리')
        SyncController().addTargetComponents(self)
        self._render()
    
    def _render(self):
        self._credentials = SyncController().getCredentials()
        self.setStyleSheet('font-size: 12px;')
        self._layout = QVBoxLayout()
        if SyncController().checkAuthorization():
            for tasklist in self._getTasklists():
                self._layout.addWidget(TasklistCheckBox(tasklist))
        self._layout.addWidget(QPushButton('저장'))
        self.setLayout(self._layout)

    def reRender(self):
        if SyncController().checkAuthorization():
            for tasklist in self._getTasklists():
                self._layout.addWidget(TasklistCheckBox(tasklist))
    
    def setCredentials(self, credentials):
        self._credentials = credentials

    def _getTasklists(self):
        result = []
        try:
            service = build('tasks', 'v1', credentials=self._credentials)
            result = [Tasklist(tasklist['id'], tasklist['title']) for tasklist in service.tasklists().list().execute().get('items', [])]
        except Exception as err:
            print(err)
        return result

class SettingFrame(QFrame):
    def __init__(self):
        super().__init__()
        self._initUI()
        
    def _initUI(self):
        self._layout = QVBoxLayout()
        self._layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self._content = QVBoxLayout()

        self._topMenu = TopMenu('setting', self)

        syncPannel = SyncPannel()
        tasklistPannel = TasklistPannel()
        self._content.addWidget(syncPannel)
        self._content.addWidget(tasklistPannel)
        
        self._layout.addWidget(self._topMenu)
        self._layout.addLayout(self._content)
        self.setLayout(self._layout)

    def x(self):
        return self.parent().x()
    
    def y(self):
        return self.parent().y()

    def move(self, x, y):
        return self.parent().move(x, y)

    def close(self):
        return self.parent().close()
        
class SettingWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._mainFrame = SettingFrame()
        self._mainFrame.setObjectName('settingWindow')
        self._mainFrame.setStyleSheet('#settingWindow { border: 1px solid #8C8C8C; background-color: white; }')
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.resize(400, 240)
        self.move(500, 500)
        self.setCentralWidget(self._mainFrame)