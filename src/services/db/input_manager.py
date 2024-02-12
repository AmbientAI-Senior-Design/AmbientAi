from src.services.db.manager import DatabaseManager


class InputManager(DatabaseManager):

    def __init__(self):
        super().__init__("ClientInput")

    def get_hrefs_for_leaderboard(self) -> list[str]:
        query = """
        SELECT * FROM input
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_input_by_id(self, id) :
        query = """
        SELECT * FROM iinput WHERE id = ?
        """

        self.cursor.execute(query, (id, ))
        return self.cursor.fetchone()
