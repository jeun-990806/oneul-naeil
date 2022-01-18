from DataTypes import Plan, Setting
import datetime
import os


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

