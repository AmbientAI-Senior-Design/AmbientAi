from src.services.db.manager import DatabaseManager
from src.models.input_model import InputModel


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
        SELECT * FROM input WHERE input_id = ?
        """

        self.cursor.execute(query, (id, ))
        return self.cursor.fetchone()

    def get_input(self) -> list[InputModel]:
        query = "SELECT * FROM input"
        self.cursor.execute(query)

        # Fetch all rows from the result set
        result = self.cursor.fetchall()

        # Create a list to store LeaderBoard objects
        leaderboard_list: list[InputModel] = []

        # Iterate over the results and create LeaderBoard objects
        for row in result:
            input_id, input_name, input_image_path, client_name, image_score = row

            leaderboard_obj = InputModel(
                image_score=image_score,
                input_name=input_name,
                input_image_path=input_image_path,
                client_name=client_name,
            )
            leaderboard_list.append(leaderboard_obj)

        return leaderboard_list

    def create_input(self, data: InputModel):
        query = "INSERT INTO input (input_name, input_image_path, client_name, image_score) VALUES (%s, %s, %s, %s)"
        res = self.cursor.execute(query, (data.input_name, data.input_image_path, data.client_name, data.image_score))
        return res
