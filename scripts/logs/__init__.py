from pathlib import Path
from datetime import datetime

LOG_LEVEL_INFO = "INFO"
LOG_LEVEL_ERROR = "ERROR"
LOG_LEVEL_WARNING = "WARNING"

class Logs:
    def __init__(self, path: Path):
        path.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        self.file_name = path / f"log_{timestamp}.txt"
        with open(self.file_name, "w") as f:
            f.write(f"[INIT] Log file created at {datetime.now()}\n")
            f.close()
            pass
    
    def write(self, message: str, level = LOG_LEVEL_INFO):
        with open(self.file_name, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now()}] [{level}] {message}\n")
            f.close()
            pass