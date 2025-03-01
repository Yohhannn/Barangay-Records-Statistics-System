import sys

from PySide6 import QtWidgets, QtGui
from PySide6.QtGui import QIcon
from PySide6.QtUiTools import QUiLoader
from Utils.utils_corner import applyRoundedCorners

# Initialize loader and application
loader = QUiLoader()
app = QtWidgets.QApplication(sys.argv)

# Functions
def load_ui(file_path):
    """Utility function to load a UI file."""
    return loader.load(file_path, None)


def setup_login_ui():
    """Setup the login UI layout and functions."""
    global window
    window = load_ui("UI/login.ui")
    window.setWindowTitle("Marigondon Barangay Profiling System")
    window.setWindowIcon(QtGui.QIcon("Assets/icon_main.png"))

    # Set images
    window.login_imageLogo.setPixmap(QtGui.QPixmap("Assets/logo_brgy.png"))
    window.login_imagePattern.setPixmap(QtGui.QPixmap("Assets/image_pattern.png"))

    # Apply rounded corners
    applyRoundedCorners(
        window.login_imagePattern,
        radius_top_left=20,
        radius_bottom_left=20,
        radius_top_right=0,
        radius_bottom_right=0,
    )

    # Connect login button
    window.login_buttonLogin.clicked.connect(login_button_clicked)


def setup_dashboard_ui():
    """Setup the dashboard UI layout and functions."""
    global window
    window = load_ui("UI/dashboard.ui")
    window.setWindowTitle("Dashboard - Marigondon Barangay Profiling System")
    window.setWindowIcon(QtGui.QIcon("Assets/icon_main.png"))

    # Set images on Navbar
    window.nav_imageLogo.setPixmap(QtGui.QPixmap("Assets/logo_brgyClear.png"))

    # Set Icons on Navbar
    window.nav_buttonDashboard.setIcon(QIcon('Assets/icon_dashboard.svg'))
    window.nav_buttonCitizenProfiles.setIcon(QIcon('Assets/icon_citizenprofiles.svg'))
    window.nav_buttonStatistics.setIcon(QIcon('Assets/icon_statistics.svg'))
    window.nav_buttonBusiness.setIcon(QIcon('Assets/icon_business.svg'))
    window.nav_buttonSchedules.setIcon(QIcon('Assets/icon_schedule.svg'))
    window.nav_buttonAdminOverview.setIcon(QIcon('Assets/icon_adminoverview_off.svg'))
    window.nav_isLocked.setIcon(QIcon('Assets/icon_isLocked.svg'))

    # Connect logout button
    window.logout_buttonLogout.clicked.connect(logout_button_clicked)


def login_button_clicked():
    """Handle login button click."""
    global window
    print("-- Login Attempt")
    print("Employee ID:", window.login_fieldEmp_id.text(), " PIN:", window.login_fieldPin.text())

    # Insert validation logic here if needed.

    # Switch to dashboard UI
    window.close()
    setup_dashboard_ui()
    window.show()


def logout_button_clicked():
    """Handle logout button click."""
    global window

    # Confirmation dialog
    confirmation = QtWidgets.QMessageBox.question(
        window,
        "Confirm Logout",
        "Are you sure you want to logout?",
        QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
    )

    if confirmation == QtWidgets.QMessageBox.Yes:
        print("-- Logout Confirmed")
        window.close()
        setup_login_ui()
        window.show()
    else:
        print("-- Logout Canceled")


# Main Program
setup_login_ui()
window.show()
app.exec()
