from datetime import datetime

def calculate_days_until(deadline_str, date_format="%Y-%m-%d"):
    """
    Returns the number of days until the deadline.
    Returns None if the format is invalid.
    """
    try:
        deadline_date = datetime.strptime(deadline_str, date_format).date()
        today = datetime.now().date()
        delta = deadline_date - today
        return delta.days
    except ValueError:
        return None

def get_urgency_color(days_left):
    """
    Returns a Tkinter-compatible color string based on the number of days left.
    """
    if days_left is None:
        return "black" # Invalid or empty date
    if days_left < 0:
        return "red" # Overdue
    elif days_left <= 2:
        return "orange" # Very Urgent
    elif days_left <= 7:
        return "goldenrod" # Upcoming
    else:
        return "forest green" # Safe
