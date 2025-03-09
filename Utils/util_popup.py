from PySide6.QtWidgets import QWidget
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

def load_popup(ui_file, parent=None):
    """
    Loads a popup widget from the given .ui file.

    Args:
        ui_file (str): Path to the .ui file.
        parent (QWidget): Parent widget (optional).

    Returns:
        QWidget: The loaded popup widget.
    """
    # Open the .ui file
    ui_file_obj = QFile(ui_file)
    ui_file_obj.open(QFile.ReadOnly)

    # Load the UI using QUiLoader
    loader = QUiLoader()
    popup = loader.load(ui_file_obj, parent)
    ui_file_obj.close()

    if not popup:
        raise ValueError(f"Failed to load UI file: {ui_file}")

    return popup
