import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    'https://www.googleapis.com/auth/tasks.readonly', 
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
        return cls._instance

    def addTasklist(self, tasklistId):
        self._targetTasklists.append(tasklistId)
    
    def removeTasklist(self, tasklistId):
        if tasklistId in self._targetTasklists:
            self._targetTasklists.remove(tasklistId)

    def saveSettingData(self, newData):
        settingData = {
            'mainwindow': (0, 0),
            'settingWindow': (0, 0)
        }
        # To-Do: 딕셔너리 형식으로 새 설정값을 받아서 이를 config.ini 파일에 업데이트
        return

    def saveUserData(self, newData):
        # To-Do: 딕셔너리 형식으로 새 설정값을 받아서 이를 localData 파일에 업데이트
        localData = {
            'tasklists': [
                {   
                    'id': '태스크리스트 아이디',
                    'title': '태스크리스트 제목',
                    'last_update': '최근 동기화 날짜',
                    'items': [
                        {
                            'id': '태스크 아이디',
                            'title': '태스크 제목',
                            'due': '설정 시간',
                            'completed': '완료 여부'
                        }
                    ]
                }
            ]
        }
        return

    def printTasklist(self):
        print(self._targetTasklists)