from PySide6.QtCore import QTimer
from datetime import datetime

def update_time_label(label):
    """Update the label with the current time."""
    now = datetime.now()
    formatted_time = now.strftime("%I:%M %p")  # Format as "10:02 PM"
    label.setText(formatted_time)
