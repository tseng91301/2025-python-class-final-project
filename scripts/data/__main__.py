from pathlib import Path
from . import UserData

if __name__ == "__main__":
    user_data = UserData()
    user_data.create(name="test2", force=True)
    pass