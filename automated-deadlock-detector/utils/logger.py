import datetime

def log(message: str, level: str = "INFO"):
    """
    Prints a timestamped log message to the console.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{level.upper()}] {message}")
