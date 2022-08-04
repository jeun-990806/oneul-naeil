from google.oauth2.credentials import Credentials
from PyQt5.QtCore import QPoint
import datetime
from typing import Union


class Task:
    def __init__(self, json:dict, category:str) -> None:
        self._taskID = json['id']
        self._etag = json['etag']
        if json['status'] == 'completed':
            self._status = True
        else:
            self._status = False
        self._title = json['title']
        self._category = category
        if 'due' in json:
            self._due = datetime.datetime.strptime(json['due'], '%Y-%m-%dT%H:%M:%S.%fZ')
        else:
            self._due = None
        self._updated = datetime.datetime.strptime(json['updated'], '%Y-%m-%dT%H:%M:%S.%fZ')
        self._dirty = False

    @property
    def taskID(self) -> str:
        return self._taskID

    @taskID.setter
    def taskID(self, taskID:str) -> None:
        self._dirty = True
        self._taskID = taskID

    @property
    def etag(self) -> str:
        return self._etag

    @etag.setter
    def etag(self, etag:str) -> None:
        self._dirty = True
        self._etag = etag

    @property
    def title(self) -> str:
        return self._title
    
    @title.setter
    def title(self, title:str) -> None:
        self._dirty = True
        self._title = title

    @property
    def status(self) -> bool:
        return self._status
    
    @status.setter
    def status(self, status:bool) -> None:
        self._dirty = True
        self._status = status
    
    @property
    def category(self) -> str:
        return self._category
    
    @category.setter
    def category(self, category:str) -> None:
        self._dirty = True
        self._category = category

    @property
    def due(self) -> Union[datetime.datetime, None]:
        return self._due

    @due.setter
    def due(self, due:Union[datetime.datetime, None]) -> None:
        self._dirty = True
        self._due = due

    @property
    def updated(self) -> datetime.datetime:
        return self._updated

    @updated.setter
    def updated(self, updated:datetime.datetime) -> None:
        self._dirty = True
        self._updated = updated

    @property
    def dirty(self) -> bool:
        return self._dirty

    def clean(self) -> None:
        self._dirty = False

    def toJSON(self) -> dict:
        jsonType = {
            'id': self._taskID,
            'etag': self._etag,
            'title': self._title,
            'updated': datetime.datetime.strftime(self._updated, '%Y-%m-%dT%H:%M:%S.%fZ'),
            'dirty': self._dirty
        }
        if self._due is not None:
            jsonType['due'] = datetime.datetime.strftime(self._due, '%Y-%m-%dT%H:%M:%S.%fZ')
        if self._status == True:
            jsonType['status'] = 'completed'
        else:
            jsonType['status'] = 'needsAction'
        return jsonType

class TaskList:
    def __init__(self, taskListID='', etag='', title='', lastUpdate=None) -> None:
        self._taskListID = taskListID
        self._etag = etag
        self._title = title
        self._lastUpdate = lastUpdate
        self._tasks = []
    
    @property
    def taskListID(self) -> str:
        return self._taskListID

    @taskListID.setter
    def taskListID(self, taskListID:str) -> None:
        self._taskListID = taskListID
    
    @property
    def etag(self) -> str:
        return self._etag

    @etag.setter
    def etag(self, etag:str) -> None:
        self._etag = etag

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, title:str) -> None:
        self._title = title
    
    @property
    def lastUpdate(self) -> datetime.datetime:
        return self._lastUpdate

    @lastUpdate.setter
    def lastUpdate(self, lastUpdate:datetime.datetime) -> None:
        self._lastUpdate = lastUpdate

    def getTask(self, taskID:str) -> Union[Task, None]:
        for task in self._tasks:
            if task.taskID == taskID:
                return task

    def addTask(self, task:Task) -> None:
        self._tasks.append(task)

    def removeTask(self, taskID:str) -> bool:
        for task in self._tasks:
            if task.taskID == taskID:
                self._tasks.remove(taskID)
                return True
        return False

# 사용자 설정 데이터.
class UserSettingData:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, credentials=None, lastSync=None, windowPositionX=0, windowPositionY=0):
        cls = type(self)
        if not hasattr(cls, '_init'):
            self._credentials = credentials
            self._lastSync = lastSync
            self._windowPositionX = windowPositionX
            self._windowPositionY = windowPositionY
            cls._init = True

    @property
    def credentials(self) -> Union[Credentials, None]:
        return self._credentials

    @credentials.setter
    def credentials(self, credentials:Credentials) -> None:
        self._credentials = credentials

    @property
    def lastSync(self) -> Union[datetime.datetime, None]:
        return self._lastSync

    @lastSync.setter
    def lastSync(self, lastSync:datetime.datetime) -> None:
        self._lastSync = lastSync

    @property
    def windowPositionX(self) -> int:
        return self._windowPositionX

    @windowPositionX.setter
    def windowPositionX(self, windowPositionX:int) -> None:
        self._windowPositionX = windowPositionX

    @property
    def windowPositionY(self) -> int:
        return self._windowPositionY

    @windowPositionY.setter
    def windowPositionY(self, windowPositionY:int) -> None:
        self._windowPositionY = windowPositionY

    
class Plan:
    def __init__(self, title):
        self.title = title
        self.checked = False


class Setting:
    def __init__(self, minimizedWindowPosX, minimizedWindowPosY, mainWindowPosX, mainWindowPosY):
        self.minimizedWindowPos = QPoint(minimizedWindowPosX, minimizedWindowPosY)
        self.mainWindowPos = QPoint(mainWindowPosX, mainWindowPosY)
