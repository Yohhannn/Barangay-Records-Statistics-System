from datetime import datetime

def update_date_label(label):
    """Update the label with the current date and day."""
    now = datetime.now()
    formatted_date = now.strftime("%b %d, %Y").upper()  # Format as "MAR 06, 2025"
    day_of_week = now.strftime("%A").upper()  # Get the day name as "THURSDAY"
    label.setText(f"{formatted_date} - {day_of_week}")
