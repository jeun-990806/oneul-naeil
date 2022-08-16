from components.buttons.IconButton import IconButton
from components.windows.SettingWindow import SettingWindow

class SettingButton(IconButton):
    def __init__(self, image='assets/images/setting.png', width=20, height=20):
        super().__init__(image=image, width=width, height=height)
        self._settingWindow = SettingWindow()

    def mousePressEvent(self, event):
        self._settingWindow.show()