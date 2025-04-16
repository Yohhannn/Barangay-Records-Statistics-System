import sys
import tkinter as tk
import ctypes
from PySide6.QtWidgets import QApplication

from Functions.citizen_functions.citizen_func import citizen_func
from Functions.dashboard_functions.dashboard_func import dashboard_func
from Functions.login_functions.login_func import LoginWindow

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


# class MainApplication(dashboard_func):
#     def __init__(self, login_window, emp_first_name):
#         super().__init__(login_window, emp_first_name)
#
#         # Initialize all screens
#         self.dashboard = dashboard_func(login_window, emp_first_name)
#         self.citizen_panel = citizen_func(login_window, emp_first_name)
#
#         # Add all screens to the stack
#         self.stack.addWidget(self.dashboard)
#         self.stack.addWidget(self.citizen_panel)
#         # Add other screens here...
#
#         # Set current widget
#         self.stack.setCurrentIndex(0)
#
#     def goto_dashboard(self):
#         """Handle navigation to dashboard screen."""
#         print("-- Navigating to Dashboard")
#         self.stack.setCurrentIndex(0)
#
#     def goto_citizen_panel(self):
#         """Handle navigation to citizen panel screen."""
#         print("-- Navigating to Citizen Panel")
#         citizen_func.setup_ui(self)
#
#         self.stack.setCurrentIndex(1)

    # Add other navigation methods here...