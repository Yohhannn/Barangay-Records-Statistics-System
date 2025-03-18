import sys
import tkinter as tk
import ctypes
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from Functions.login_reg_func import LoginWindow

# Initialize Tkinter (if you need it)
root = tk.Tk()

# Set Windows App ID (for taskbar grouping)
myappid = "mycompany.myproduct.subproduct.version"  # Arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

# Hide Tkinter window (since you're using PySide6 for UI)
root.withdraw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()

    sys.exit(app.exec())