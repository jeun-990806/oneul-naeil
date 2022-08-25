import sys
from PyQt5.QtWidgets import QApplication
from MainWindow import Main

app = QApplication(sys.argv)
mainWindow = Main()
mainWindow.show()
sys.exit(app.exec_())
