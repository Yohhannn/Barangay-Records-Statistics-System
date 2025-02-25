import sys
from PySide6 import QtWidgets, QtGui
from PySide6.QtUiTools import QUiLoader
from Utils.utils_corner import applyRoundedCorners

loader = QUiLoader()
app = QtWidgets.QApplication(sys.argv)
window = loader.load("UI/login.ui", None)

# Functions
def login_Button() :
    print("-- Login Attempt")
    print("Employee ID:", window.login_fieldEmp_id.text(), " PIN:", window.login_fieldPin.text())


# Images Used -- Manually Refer the component named login_imageLogo to the logo
window.login_imageLogo.setPixmap(QtGui.QPixmap("Assets/logo_brgy.png"))
window.login_imagePattern.setPixmap(QtGui.QPixmap("Assets/image_pattern.png"))

# Utility Applied -- Layout Modifications
applyRoundedCorners(window.login_imagePattern, radius_top_left=20, radius_bottom_left=20, radius_top_right=0, radius_bottom_right=0)

# Program Icon -- Set
window.setWindowIcon(QtGui.QIcon("Assets/icon_main.png"))

# Program Title -- Set
window.setWindowTitle("Marigondon Barangay Profiling System")

# Applied Functions
window.login_buttonLogin.clicked.connect(login_Button)
window.show()
app.exec()