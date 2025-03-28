import sys
import tkinter as tk
import ctypes
from PySide6.QtWidgets import QApplication

from Functions.login_functions.login_func import login_func

# Initialize Tkinter (if you need it)
root = tk.Tk()

# Set Windows App ID (for taskbar grouping)
myappid = "mycompany.myproduct.subproduct.version"  # Arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

# Hide Tkinter window (since you're using PySide6 for UI)
root.withdraw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = login_func()
    login_window.show()

    sys.exit(app.exec())