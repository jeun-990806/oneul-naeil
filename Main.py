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

sys.exit(app.exec_())
