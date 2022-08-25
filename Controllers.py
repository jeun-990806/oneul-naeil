import os
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = [
    'https://www.googleapis.com/auth/tasks', 
    'https://www.googleapis.com/auth/userinfo.email', 
    'https://www.googleapis.com/auth/userinfo.profile',
    'openid'
    ]

class SyncController:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
            cls._credentials = None
            cls._components = []
        return cls._instance

    def addTargetComponents(self, target):
        self._components.append(target)
    
    def checkAuthorization(self):
        if os.path.exists('token.json'):
            self._credentials = Credentials.from_authorized_user_file('token.json', SCOPES)
        if not self._credentials or not self._credentials.valid:
            if self._credentials and self._credentials.expired and self._credentials.refresh_token:
                self._credentials.refresh(Request())
            else:
                return False
        return True

    def authorize(self):
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        self._credentials = flow.run_local_server(port=0)
        for component in self._components:
            component.setCredentials(self._credentials)
            component.reRender()
        with open('token.json', 'w') as token:
            token.write(self._credentials.to_json())

    def getCredentials(self):
        return self._credentials

class DataController:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
            cls._targetTasklists = []
            cls._targetComponents = []
        return cls._instance

    def getTargetTasklists(self):
        return self._targetTasklists

    def attach(self, component):
        if component not in self._targetComponents:
            self._targetComponents.append(component)

    def update(self):
        for component in self._targetComponents:
            component.updateState()

    def loadAllTask(self):
        for tasklist in self._targetTasklists:
            tasklist['items'] = self.loadTasklistItems(tasklist['id'])

    def loadTasklistItems(self, tasklistId):
        credentials = SyncController().getCredentials()
        if credentials:
            service = build('tasks', 'v1', credentials=credentials)
            return service.tasks().list(tasklist=tasklistId).execute().get('items', [])

    def addTasklist(self, tasklist):
        if tasklist not in self._targetTasklists:
            self._targetTasklists.append(tasklist)
    
    def removeTasklist(self, tasklist):
        for tl in self._targetTasklists:
            if tl['id'] == tasklist['id']:
                self._targetTasklists.remove(tl)
                break

    def saveSettingData(self, newData):
        settingData = {
            'mainwindow': (0, 0),
            'settingWindow': (0, 0)
        }
        # To-Do: 딕셔너리 형식으로 새 설정값을 받아서 이를 config.ini 파일에 업데이트
        return

    def saveUserData(self):
        userDataFilePath = 'localData.json'
        with open(userDataFilePath, 'w') as file:
            json.dump(self._targetTasklists, file)
    
    def loadUserData(self):
        userDataFilePath = 'localData.json'
        with open(userDataFilePath, 'r') as file:
            self._targetTasklists = json.load(file)
    
    def checkSync(self, tasklistId):
        if tasklistId in [tasklist['id'] for tasklist in self._targetTasklists]:
            return True
        return False
    
    def getTasklistItems(self, index):
        return self._targetTasklists[index]['items']

    def getAllTasklistItems(self):
        result = []
        for tasklist in self._targetTasklists:
            result += tasklist['items']
        return result

    def getTasklist(self, taskId):
        result = None
        for tasklist in self._targetTasklists:
            for task in tasklist['items']:
                if task['id'] == taskId:
                    result = tasklist
        return result

    def updateTask(self, tasklistId, taskJson):
        targetTasklist = None
        targetTask = None
        for tasklist in self._targetTasklists:
            targetTasklist = tasklist
            if tasklist['id'] == tasklistId:
                for task in tasklist['items']:
                    if task['id'] == taskJson['id']:
                        targetTask = task
                        break
                break
        targetTasklist['items'][targetTasklist['items'].index(targetTask)] = taskJson
        credentials = SyncController().getCredentials()
        if credentials:
            service = build('tasks', 'v1', credentials=credentials)
            service.tasks().update(tasklist=tasklistId, task=taskJson['id'], body=taskJson).execute()
        DataController().saveUserData()
        
    def deleteTask(self, tasklistId, taskJson):
        targetTasklist = None
        targetTask = None
        for tasklist in self._targetTasklists:
            if tasklist['id'] == tasklistId:
                targetTasklist = tasklist
                for task in tasklist['items']:
                    if task['id'] == taskJson['id']:
                        targetTask = task
                        break
                break
        targetTasklist['items'].remove(targetTask)
        credentials = SyncController().getCredentials()
        if credentials:
            service = build('tasks', 'v1', credentials=credentials)
            service.tasks().delete(tasklist=tasklistId, task=taskJson['id']).execute()
        DataController().saveUserData()

    def addTask(self, tasklistId, taskJson=None):
        if taskJson is None:
            taskJson = {
                "title": "Untitled",
                "status": "needsAction",
                }
        credentials = SyncController().getCredentials()
        if credentials:
            service = build('tasks', 'v1', credentials=credentials)
            result = service.tasks().insert(tasklist=tasklistId, body=taskJson).execute()
            for tasklist in self._targetTasklists:
                if tasklist['id'] == tasklistId:
                    tasklist['items'].append(result)
            self.update()
            self.saveUserData()
    
    def moveTask(self, originTasklistId, destTasklistId, taskJson):
        self.deleteTask(originTasklistId, taskJson)
        self.addTask(destTasklistId, taskJson=taskJson)

    def printTasklist(self):
        print(self._targetTasklists)