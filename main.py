from scripts.logs import Logs
from scripts.genai import GenAI
from pathlib import Path

project_root = Path(__file__).parent

logs = Logs(project_root / "logs")

logs.write("ABC")