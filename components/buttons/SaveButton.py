from components.buttons.IconButton import IconButton

class SaveButton(IconButton):
    def __init__(self, image='assets/images/save.png', width=20, height=20):
        super().__init__(image=image, width=width, height=height)

    def mousePressEvent(self, event):
        print('yeah')
