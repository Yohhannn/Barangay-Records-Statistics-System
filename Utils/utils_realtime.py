from PySide6.QtCore import QTimer
from datetime import datetime

def update_time_label(label):
    """Update the label with the current time, including seconds."""
    now = datetime.now()
    formatted_time = now.strftime("%I:%M:%S %p")  # Format as EX: "10:02:45 PM"
    label.setText(formatted_time)