from datetime import datetime

def get_current_time() -> str:
    """Returns the current time in a human-readable format."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")