from pathlib import Path
from datetime import datetime

class Logs:
    def __init__(self, path: Path):
        path.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        self.file_name = path / f"log_{timestamp}.txt"
        with open(self.file_name, "w") as f:
            f.write(f"[INIT] Log file created at {datetime.now()}\n")
            f.close()
            pass
    
    def write(self, message: str):
        with open(self.file_name, "a") as f:
            f.write(f"[{datetime.now()}] {message}\n")
            f.close()
            pass

if __name__ == "__main__":
    project_root = Path(".").parent

    logs = Logs(project_root / "logs")

    logs.write("ABC")