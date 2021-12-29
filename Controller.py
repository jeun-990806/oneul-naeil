from DataTypes import Plan, Setting
import time


class Controller:
    def __init__(self, model, view):
        self._model = model
        self._view = view
        self._view.setController(self)

    def initController(self):
        self._model.setDate(time.time())
        self.setWindowPosition()

    def loadWindowPosition(self):
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

    def setWindowPosition(self):
        self._model.setSettingData(self.loadWindowPosition())
        self._view.setMinimizedWindowPosition(self._model.getSettingData().minimizedWindowPos)
        self._view.setMainWindowPosition(self._model.getSettingData().mainWindowPos)

    def addPlan(self, title):
        plan = Plan(title)
        self._view.addPlanWidget(plan)
        self._model.addPlan(plan)

    def renamePlan(self, plan, title):
        self._model.updatePlan(plan, title, plan.checked)

    def changePlanState(self, plan):
        self._model.updatePlan(plan, plan.title, not plan.checked)
        return plan.checked

    def removePlan(self, plan):
        self._model.removePlan(plan)
        self.printPlans()

    def printPlans(self):
        print(self._model.getDate())
        for plan in self._model.getPlanData():
            if plan.checked:
                print('[*]', end=' ')
            else:
                print('[ ]', end=' ')
            print(plan.title)

    def close(self):
        self.saveWindowPosition()
        del self._model
        del self._view
        del self

