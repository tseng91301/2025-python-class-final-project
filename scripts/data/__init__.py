import json
from pathlib import Path
from datetime import datetime

class Conversation:
    dt: datetime
    prompt: str
    ai_return: dict
    def from_dict(self, j: dict):
        self.dt = datetime.fromisoformat(j["dateTime"])
        self.prompt = j["prompt"]
        self.ai_return = j["ai_return"]
        pass
    def __init__(self, j: dict = None, p: str = None, r: dict = None):
        if not j is None:
            self.from_dict(j=j)
        else:
            self.dt = datetime.now()
            self.prompt = p
            self.ai_return = r
    def output(self):
        return {
            "dateTime": self.dt.isoformat(),
            "prompt": self.prompt,
            "ai_return": self.ai_return
        }
    def __str__(self):
        return json.dumps(self.output(), indent=2, ensure_ascii=False)
    
class Note:
    dt: datetime
    text: str
    mood_score: float
    def from_dict(self, j: dict):
        self.dt = datetime.fromisoformat(j["dateTime"])
        self.text = j["text"]
        self.mood_score = j["mood_score"]
        pass
    def __init__(self, j: dict = None, t: str = None, mood_score: float = 0):
        if not j is None:
            self.from_dict(j=j)
        else:
            self.text = t
            self.mood_score = mood_score
            self.dt = datetime.now()
    def output(self):
        return {
            "dateTime": self.dt.isoformat(),
            "text": self.text,
            "mood_score": self.mood_score
        }
    def __str__(self):
        return json.dumps(self.output(), indent=2, ensure_ascii=False)

class UserData:
    storage_path: Path
    notes_export_path: Path
    name: str = ""
    description: str = ""
    notes = list[Note]
    conversations = list[Conversation]
    def __init__(self, base_path: Path):
        self.storage_path = base_path / "data/saves"
        self.notes_export_path = base_path / "output/notes"
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.notes_export_path.mkdir(parents=True, exist_ok=True)
    def create(self, name: str, force: bool = False):
        if force or not Path(self.storage_path/f"{name}.json").exists():
            with open(f"{self.storage_path}/{name}.json", "w") as f:
                f.write(json.dumps({}))
                f.close()
                pass
            self.name = name
            self.description = ""
            self.notes = []
            self.conversations = []
            self.save()
            print(f"{name}'s data has been created.")
            pass
        else:
            self.load(name=name)
        pass

    def load(self, name: str):
        with open(f"{self.storage_path}/{name}.json", "r", encoding="utf-8") as f:
            data = json.loads(f.read())
            self.name = data["name"]
            self.description = data["description"]
            self.notes = [Note(j=n) for n in data["notes"]]
            self.conversations = [Conversation(j=c) for c in data["conversations"]]
            f.close()
            pass

    def add_note(self, note: Note):
        self.notes.append(note)
        self.save()
        return

    def add_conversation(self, c: Conversation):
        self.conversations.append(c)
        if c.ai_return["description"] != "N/A":
            self.description = c.ai_return["description"]
        self.save()
        return

    def save(self):
        if self.name == "":
            raise Exception("No name set")
        with open(f"{self.storage_path}/{self.name}.json", "w", encoding="utf-8") as f:
            f.write(json.dumps({
                "name": self.name,
                "description": self.description,
                "notes": [n.output() for n in self.notes],
                "conversations": [c.output() for c in self.conversations]
            }, indent=2, ensure_ascii=False))
            f.close()
            pass
    
    def export_notes(self):
        timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        file_name = f"notes_{self.name}_{timestamp}.txt"
        file_path = self.notes_export_path / file_name
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"{self.name}'s notes:\n")
            f.close()
        with open(file_path, "a", encoding="utf-8") as f:
            for note in self.notes:
                d = note.output()
                f.write(f"[{d["dateTime"]}]:\n  {d["text"]}\n  Mood Score: {d["mood_score"]}\n")
            f.close()