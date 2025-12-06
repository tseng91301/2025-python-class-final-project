import json
from pathlib import Path
from datetime import datetime

class UserData:
    storage_path = Path("./data/saves")
    name: str = ""
    description: str = ""
    notes = []
    def create(self, name: str, force: bool = False):
        if force or not Path(self.storage_path/f"{name}.json").exists():
            with open(f"{self.storage_path}/{name}.json", "w") as f:
                f.write(json.dumps({}))
                f.close()
                pass
            self.name = name
            self.description = ""
            self.notes = []
            self.save()
            print(f"{name}'s data has been created.")
            pass
        else:
            raise Exception("File already exists")
        pass

    def load(self, name: str):
        with open(f"{self.storage_path}/{name}.json", "r") as f:
            data = json.loads(f.read())
            f.close()
            self.name = data["name"]
            self.description = data["description"]
            self.notes = data["notes"]
            pass

    def add_note(self, note: dict):
        self.notes.append(note)
        self.save()
        pass

    def save(self):
        if self.name == "":
            raise Exception("No name set")
        with open(f"{self.storage_path}/{self.name}.json", "w") as f:
            f.write(json.dumps({
                "name": self.name,
                "description": self.description,
                "notes": self.notes
            }, indent=2))
            f.close()
            print(f"{self.name}'s data has been saved.")
            pass