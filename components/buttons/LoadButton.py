from components.buttons.IconButton import IconButton

class LoadButton(IconButton):
    def __init__(self, image='assets/images/load.png', width=20, height=20):
        super().__init__(image=image, width=width, height=height)

    def mousePressEvent(self, event):
        print('yeah')
