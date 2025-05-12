from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from PySide6.QtWidgets import QWidget

def load_ui_widget(ui_path: str, parent=None) -> QWidget:
    loader = QUiLoader()
    file = QFile(ui_path)
    file.open(QFile.ReadOnly)
    widget = loader.load(file, parent)
    file.close()
    return widget
