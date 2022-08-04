from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QMouseEvent

# 이미지 버튼 위젯
# - 클릭, 드래그 가능
# - 이미지 크기 설정 가능

class IconButton(QLabel):
    def __init__(self, image:str, width=20, height=20):
        super().__init__()
        self.setPixmap(QPixmap(image))
        self.setFixedHeight(width)
        self.setFixedWidth(height)
    
    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        super().mouseMoveEvent(event)