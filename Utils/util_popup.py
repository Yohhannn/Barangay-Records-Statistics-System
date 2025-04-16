from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from PySide6.QtWidgets import QWidget

def load_popup(ui_file_path: str, parent: QWidget = None):
    loader = QUiLoader()
    file = QFile(ui_file_path)
    file.open(QFile.ReadOnly)
    popup = loader.load(file, parent)
    file.close()
    return popup
