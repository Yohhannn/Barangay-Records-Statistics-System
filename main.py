import sys
from PySide6 import QtWidgets
from PySide6.QtUiTools import QUiLoader

loader = QUiLoader()

app = QtWidgets.QApplication(sys.argv)
window = loader.load("UI/test_login_v2.ui", None)

def test() :
    print("-- Login Attempt")
    print("Employee ID:", window.line_edit_emp_id.text(), " PIN:", window.line_edit_emp_pin.text())



window.setWindowTitle("Marigondon Barangay Profiling System")

window.push_button_login.clicked.connect(test)
window.show()
app.exec()