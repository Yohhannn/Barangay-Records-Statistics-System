import sys
from PySide6 import QtWidgets, QtGui
from PySide6.QtUiTools import QUiLoader

loader = QUiLoader()

app = QtWidgets.QApplication(sys.argv)
window = loader.load("UI/login.ui", None)

def login_Button() :
    print("-- Login Attempt")
    print("Employee ID:", window.login_fieldEmp_id.text(), " PIN:", window.login_fieldPin.text())

# Manually Refer the component named login_imageLogo to the logo
window.login_imageLogo.setPixmap(QtGui.QPixmap("Assets/logo_brgy.png"))
window.setWindowIcon(QtGui.QIcon("Assets/icon_main.png"))
window.setWindowTitle("Marigondon Barangay Profiling System")

window.login_buttonLogin.clicked.connect(login_Button)
window.show()
app.exec()