from pathlib import Path
from . import Logs

if __name__ == "__main__":
    project_root = Path(".").parent

    logs = Logs(project_root / "logs")

    logs.write("ABC")