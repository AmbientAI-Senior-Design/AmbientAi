from src.models import InputModel
from src.services.db.input_manager import InputManager

def create_leaderboard():
    pass


def get_leaderboard() -> list[InputModel]:
    with InputManager() as db:
        rows = db.get_input()
        return rows
