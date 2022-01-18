import sys
from PyQt5.QtWidgets import QApplication

from Model import Model
from View import View
from Controller import Controller

app = QApplication(sys.argv)

model = Model()
view = View()
controller = Controller(model, view)
controller.initController()
if len(sys.argv) == 2:
    controller.loadPlanData(sys.argv[1])

sys.exit(app.exec_())
