from PyQt5.QtCore import QPoint


class Plan:
    def __init__(self, title):
        self.title = title
        self.checked = False


class Setting:
    def __init__(self, minimizedWindowPosX, minimizedWindowPosY, mainWindowPosX, mainWindowPosY):
        self.minimizedWindowPos = QPoint(minimizedWindowPosX, minimizedWindowPosY)
        self.mainWindowPos = QPoint(mainWindowPosX, mainWindowPosY)
