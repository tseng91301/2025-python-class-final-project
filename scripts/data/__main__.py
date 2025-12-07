from pathlib import Path
import json
from . import UserData, Note, Conversation

if __name__ == "__main__":
    user_data = UserData(base_path=Path("."))
    user_data.create(name="test2", force=True)
    user_data.add_note(Note("This is a test note", 35))
    user_data.add_note(Note("這是一個中文筆記", 0))
    user_data.add_conversation(Conversation(p="My text input towards AI", r=json.dumps({
        "response": "This is a response text from AI.",
        "mood_value": 40.0,
        "description": "Description given by AI."
    })))
    user_data.export_notes()
    pass