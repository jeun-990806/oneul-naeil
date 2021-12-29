class Model:
    def __init__(self):
        self._date = None
        self._plans = []
        self._setting = None

    def getDate(self):
        return self._date

    def getSettingData(self):
        return self._setting

    def getPlanData(self):
        return self._plans

    def setDate(self, date):
        self._date = date

    def setSettingData(self, setting):
        self._setting = setting

    def addPlan(self, plan):
        self._plans.append(plan)

    def updatePlan(self, plan, title, state):
        plan.title = title
        plan.checked = state

    def removePlan(self, plan):
        self._plans.remove(plan)
