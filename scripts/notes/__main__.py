from pathlib import Path
from ..logs import Logs
from . import Notes  # 假設 Notes 類別在 __init__.py

if __name__ == "__main__":
    project_root = Path(__file__).parent.parent.parent
    log = Logs(Path(f"{project_root}/logs"))
    notes = Notes(Path(f"{project_root}/notes"), "demo", log)

    notes.write("第一個測試 note")
    notes.write("第二個測試 note")

    print("目前 notes：")
    for n in notes.notes:
        print(n)

    notes.save_notes()
    print("notes 已儲存！")
