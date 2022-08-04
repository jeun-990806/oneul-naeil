from PyQt5.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from components.buttons.IconButton import IconButton
from components.frames.TaskWidget import TaskWidget

class TaskWidgetList(QFrame):
    def __init__(self, parent=None, controller=None, category=''):
        super().__init__(parent)
        self.setFrameShape(QFrame.Box)
        self.setLineWidth(1)

        self._controller = controller

        categoryTitle = QHBoxLayout()
        
        self._list = QLabel(category, self)
        self._list.setFont(QFont('돋움', 7))
        self._addButton = IconButton('resources/add.png')
        categoryTitle.addWidget(self._list, alignment=Qt.AlignmentFlag.AlignLeft)
        categoryTitle.addWidget(self._addButton, alignment=Qt.AlignmentFlag.AlignRight)

        self._layout = QVBoxLayout(self)
        self._layout.addLayout(categoryTitle)
        self._layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self._loadPlans()

    def _loadPlans(self):
        try:
            planDataList = [
                {'title': 'abcd', 'status': False}
                ] #self._controller.getPlanData()
            for planData in planDataList:
                self.addPlanWidget(planData)
        except:
            print("There is no proper controller.")
    
    def addPlanWidget(self, planData):
        try:
            planWidget = self._createPlanWidget(planData)
            self._layout.addLayout(planWidget)
        except:
            print("Cannot make a planwidget from this data: ", planData)

    def _createPlanWidget(self, planData):
        return TaskWidget(title=planData['title'], status=planData['status'])