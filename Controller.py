from http import server
from typing import Union
from DataTypes import Plan, Setting, Task
import datetime
import time
import os
import os.path
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


SCOPES = ['https://www.googleapis.com/auth/tasks.readonly', 'https://www.googleapis.com/auth/userinfo.email', 'openid']
FILE_PATH = {
    'credentials': 'onnl/credentials/credentials.json',
    'token': 'onnl/credentials/token.json',
    'local': 'onnl/data/local.json',
    'state': 'onnl/data/taskState.json'
}
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = FILE_PATH['credentials']


class MainController:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        cls = type(self)
        if not hasattr(cls, '_init'):
            cls._init = True
            self._credentials = None
            self._localData = self._loadLocalData()
            self._localTasklist = []

    def _doAuthorize(self) -> Union[Credentials, None]:
        credentials = None

        if os.path.exists(FILE_PATH['token']):
            credentials = Credentials.from_authorized_user_file(FILE_PATH['token'], SCOPES)
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(FILE_PATH['credentials'], SCOPES)
                credentials = flow.run_local_server(port=0)
            with open(FILE_PATH['token'], 'w') as token:
                token.write(credentials.to_json())
        
        return credentials

    def _loadLocalData(self) -> dict:
        localData = {}

        if not os.path.exists(FILE_PATH['local']):
            return self._createLocalData()    
        with open(FILE_PATH['local']) as dataFile:
            localData = json.load(dataFile)

        return localData

    def _createLocalData(self) -> dict:
        initLocalData = {
            "email": None,
            "windowPositionX": 0,
            "windowPositionY": 0,
            "taskList": [],
            "lastUpdated": None
        }

        with open(FILE_PATH['local'], 'w') as dataFile:
            json.dump(initLocalData, dataFile, indent=2)
        return initLocalData

    def login(self) -> bool:
        self._credentials = self._doAuthorize()
        if self._credentials is not None:
            try:
                if self._localData['email'] is not None:
                    # Already logged in.
                    raise Exception
                service = build('oauth2', 'v2', credentials=self._credentials)
                userInfo = service.userinfo().get().execute()
            except:
                return False
            self._localData['email'] = userInfo['email']

    def logout(self) -> bool:
        if self._credentials is None and self._localData['email'] is None:
            # Already logged out.
            return False
        else:
            self._credentials = None
            self._localData['email'] = None
            self._localData['taskList'] = []
            return True
        
    def getLocalData(self) -> dict:
        return self._localData

    def saveLocalData(self) -> bool:
        with open(FILE_PATH['local'], 'w') as dataFile:
            json.dump(self._localData, dataFile, indent=2)

    def getLocalTasks(self) -> dict:
        return self._localTasklist

    def getTaskList(self) -> str:
        service = build('tasks', 'v1', credentials=self._credentials)
        tasklists = service.tasklists().list().execute()
        tasklistsStr = ''

        for tasklist in tasklists.get('items', []):
            tasklistsStr += tasklist['title'] + '(' + tasklist['id'] + ')\n'

        return tasklistsStr

    def addTaskList(self, tasklistID: str) -> bool:
        try:
            service = build('tasks', 'v1', credentials=self._credentials)
            targetTasklist = service.tasklists().get(tasklist=tasklistID).execute()

            if targetTasklist['id'] in [tasklist['id'] for tasklist in self._localData['taskList']]:
                # Already added tasklist.
                raise Exception
            self._localData['taskList'].append(targetTasklist)
            self._localData['lastUpdated'] = datetime.datetime.now()
            return True
        except:
            return False

    def deleteTaskList(self, tasklistID: str) -> bool:
        try:
            for tasklist in self._localData['taskList']:
                if tasklist['id'] == tasklistID:
                    targetTasklist = tasklist
                    break
            self._localData['taskList'].remove(targetTasklist)
            return True
        except:
            return False

    def getTasks(self, tasklist: str, minDueDate: datetime=None, maxDueDate: datetime=None, showCompleted: bool=True, showDeleted: bool=False) -> list:
        try:
            service = build('tasks', 'v1', credentials=self._credentials)
            if minDueDate is None:
                minDueDate = ''
            else:
                minDueDate = minDueDate.strftime('%Y-%m-%dT00:00:00.000Z')
            if maxDueDate is None:
                maxDueDate = ''
            else:
                maxDueDate = maxDueDate.strftime('%Y-%m-%dT00:00:00.000Z')
            tasks = service.tasks().list(tasklist=tasklist, dueMin=minDueDate, dueMax=maxDueDate, showCompleted=showCompleted, showDeleted=showDeleted, showHidden=True).execute().get('items', [])
            print("태스크 JOSN DATA 전처리")
            processedTasks = []
            for task in tasks:
                processedTasks.append(
                    {
                        'tasklist': tasklist,
                        'id': task.get('id'), 
                        'etag': task.get('etag'), 
                        'title': bytes(task.get('title'), 'utf-8').decode('utf-8'),
                        'status': task.get('status'),
                        'due': task.get('due'),
                        'completed': task.get('completed'),
                        'updated': datetime.datetime.strptime(task.get('updated'), '%Y-%m-%dT%H:%M:%S.000Z')
                    }
                )
            self._localData['lastUpdated'] = datetime.datetime.now()
            return processedTasks
        except Exception as e:
            print(e)
            return []

    def addTasks(self, tasks: list) -> bool:
        try:
            for task in tasks:
                self._localTasklist.append(task)
            return True
        except:
            return False

    def updateTask(self, id: str, title: str=None, status: bool=None, delete: bool=False):
        # updateTask(): 로컬 태스크 리스트에 있는 태스크 정보를 수정한다. (구글 태스크에 바로 요청을 보내지 않음!)
        for task in self._localTasklist:
            if task['id'] == id:
                if title is not None:
                    task['title'] = title
                if status is not None and status:
                    task['status'] = 'completed'
                elif status is not None and not status:
                    task['status'] = 'needsAction'
                if delete:
                    task['deleted'] = True
                task['updated'] = datetime.datetime.now()
                break
    
    def createTask(self, title: str='untitled', status: bool=False, dueDate: str=None) -> dict:
        # 태스크 정보를 받아 JSON 생성
        newTask = {}
        newTask['id'] = str(time.time())
        newTask['tasklist'] = 'local'
        newTask['title'] = title
        if status:
            newTask['status'] = 'completed'
        else:
            newTask['status'] = 'needsAction'
        
        if dueDate is not None:
            newTask['due'] = dueDate + 'T00:00:00.000Z'
        
        newTask['updated'] = datetime.datetime.now()

        return newTask

    def sync(self):
        print("동기화 대상: ")
        if self._localData['lastUpdated'] is not None:
            for task in self._localTasklist:
                if task['updated'] > self._localData['lastUpdated']:
                    print(task['title'], '(' + task['id'] + ')')


class Controller:
    def __init__(self, model, view):
        self._model = model
        self._view = view
        self._view.setController(self)

    def initController(self):
        self._model.setDate(datetime.datetime.now())
        self.setWindowPosition()

    def loadWindowPosition(self):
        if not os.path.exists('config.ini'):
            return Setting(0, 0, 0, 0)
        configFile = open('config.ini', 'r').readlines()
        minimizedWindowPosX = 0
        minimizedWindowPosY = 0
        mainWindowPosX = 0
        mainWindowPosY = 0
        for line in configFile:
            line = line.replace('\n', '')
            value = line.split('=')[1]
            if 'MinimizedWindowPosX' in line:
                minimizedWindowPosX = int(value)
            elif 'MinimizedWindowPosY' in line:
                minimizedWindowPosY = int(value)
            elif 'MainWindowPosX' in line:
                mainWindowPosX = int(value)
            elif 'MainWindowPosY' in line:
                mainWindowPosY = int(value)
        return Setting(minimizedWindowPosX, minimizedWindowPosY, mainWindowPosX, mainWindowPosY)
    
    def loadPlanData(self, fileName):
        with open(fileName, 'r') as loadedFile:
            data = loadedFile.readlines()
            for line in data[1:]:
                if line.startswith('[*]'):
                    checked = True
                else:
                    checked = False
                self.addPlan(line[line.index(']') + 1:].replace('\n', ''), checked=checked, initEditable=False)

    def saveWindowPosition(self):
        with open('config.ini', 'w') as configFile:
            minimizedWindowPos = self._view.getMinimizedWindowPosition()
            mainWindowPos = self._view.getMainWindowPosition()
            configFile.write('MinimizedWindowPosX=')
            configFile.write(str(minimizedWindowPos.x()))
            configFile.write('\nMinimizedWindowPosY=')
            configFile.write(str(minimizedWindowPos.y()))
            configFile.write('\nMainWindowPosX=')
            configFile.write(str(mainWindowPos.x()))
            configFile.write('\nMainWindowPosY=')
            configFile.write(str(mainWindowPos.y()))

    def savePlanData(self):
        with open(self._model.getDate().strftime("%Y-%m-%d") + '.pln', 'w') as savedFile:
            savedFile.write(self.makePlanDataToStr())

    def setWindowPosition(self):
        self._model.setSettingData(self.loadWindowPosition())
        self._view.setMinimizedWindowPosition(self._model.getSettingData().minimizedWindowPos)
        self._view.setMainWindowPosition(self._model.getSettingData().mainWindowPos)

    def addPlan(self, title, checked=False, initEditable=True):
        plan = Plan(title)
        plan.checked = checked
        self._view.addPlanWidget(plan, initEditable)
        self._model.addPlan(plan)

    def renamePlan(self, plan, title):
        self._model.updatePlan(plan, title, plan.checked)

    def changePlanState(self, plan):
        self._model.updatePlan(plan, plan.title, not plan.checked)
        return plan.checked

    def removePlan(self, plan):
        self._model.removePlan(plan)

    def makePlanDataToStr(self):
        result = self._model.getDate().strftime("%Y-%m-%d")
        for plan in self._model.getPlanData():
            result += '\n'
            if plan.checked:
                result += '[*]'
            else:
                result += '[ ]'
            result += plan.title
        return result

    def close(self):
        self.saveWindowPosition()
        del self._model
        del self._view
        del self

