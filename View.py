from Widgets import MainFrame, MinimizedFrame


class View:
    def __init__(self):
        self._controller = None
        self._window = MainFrame(self)
        self._icon = MinimizedFrame(self, self._window)

    def setController(self, controller):
        self._controller = controller

    def getMinimizedWindowPosition(self):
        return self._icon.mapToGlobal(self._icon.rect().topLeft())

    def getMainWindowPosition(self):
        return self._window.mapToGlobal(self._window.rect().topLeft())

    def setMinimizedWindowPosition(self, pos):
        self._icon.setPosition(pos)

    def setMainWindowPosition(self, pos):
        self._window.setPosition(pos)

    def addPlan(self):
        self._controller.addPlan('untitled')

    def renamePlan(self, plan, title):
        self._controller.renamePlan(plan, title)

    def getFittedWidth(self, text):
        self._controller.getFittedWidth(text)

    def changePlanState(self, plan):
        return self._controller.changePlanState(plan)

    def removePlan(self, plan):
        self._controller.removePlan(plan)

    def addPlanWidget(self, plan, initEditable=True):
        self._window.addPlanWidget(plan, initEditable=initEditable)

    def savePlanData(self):
        self._controller.savePlanData()

    def close(self):
        self._window.close()
        self._icon.close()
        self._controller.close()
