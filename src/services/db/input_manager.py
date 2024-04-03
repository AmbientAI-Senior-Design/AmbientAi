from src.services.db.manager import DatabaseManager
from src.models.input_model import InputModel
import mysql.connector

# a get request


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

    def get_current_score(self):
        query = "SELECT image_score FROM input ORDER BY input_id DESC LIMIT 1"
        try:
            with self:  # This will call __enter__ method to set up the connection and cursor
                self.cursor.execute(query)
                res = self.cursor.fetchone()
            # The __exit__ method will be called here, closing the cursor and connection
            return res[0] if res else 0
        except mysql.connector.Error as err:
            print(f"Error fetching current score: {err}")
            return 0

    def create_input(self, data: InputModel):
        query = "INSERT INTO input (input_id, input_name, input_image_path, client_name, image_score) VALUES (%s, %s, %s, %s, %s)"
        res = self.cursor.execute(query, (data.input_id, data.input_name, data.input_image_path, data.client_name, data.image_score))
        return res

    def get_highest_ranked_input_src(self) -> str:
        query = "SELECT input_image_path FROM input ORDER BY image_score DESC LIMIT 1"
        try:
            with self:  # This will call __enter__ method to set up the connection and cursor
                self.cursor.execute(query)
                res = self.cursor.fetchone()
            # The __exit__ method will be called here, closing the cursor and connection
            return res[0] if res else None
        except mysql.connector.Error as err:
            print(f"Error fetching highest ranked input src: {err}")
            return None

    def get_all_input_srcs(self) -> list[str]:
        query = f"SELECT input_image_path FROM input"
        self.cursor.execute(query)
        res = self.cursor.fetchall()
        return res

    def update_engagement(self, input_id: int, score: int):
        query = "UPDATE input SET image_score = %s WHERE input_id = %s"
        self.cursor.execute(query, (score, input_id))

    def input_id_exist(self):
        query = "SELECT EXISTS(SELECT 1 FROM input)"
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]
    
    def leaderboard_data(self): # gathers data for leaderboard.html
        query = "SELECT input_name, image_score FROM input"
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        return data

    def insert_engagement_report(self, date, duration, numberOfPeople, numberOfEngagedPeople, score, slideId, index):
        query = """
        INSERT INTO EngagementReport (date, duration, numberOfPeople, numberOfEngagedPeople, score, slideId, `index`)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        try:
            with self:
                self.cursor.execute(query, (date, duration, numberOfPeople, numberOfEngagedPeople, score, slideId, index))
                self._conn.commit()
        except mysql.connector.Error as err:
            print(f"Error inserting engagement report: {err}")

    def clean_database(self, before_date):
        query = "DELETE FROM EngagementReport WHERE date < %s"
        try:
            with self:
                self.cursor.execute(query, (before_date,))
                self._conn.commit()
        except mysql.connector.Error as err:
            print(f"Error cleaning database: {err}")

    def get_leaderboard_content(self):
        query = """
        SELECT slideId, AVG(score) as averageScore
        FROM EngagementReport
        GROUP BY slideId
        ORDER BY averageScore DESC
        """
        leaderboard_data = []
        try:
            with self:
                self.cursor.execute(query)
                for (slideId, averageScore) in self.cursor:
                    leaderboard_data.append({"slideId": slideId, "averageScore": averageScore})
        except mysql.connector.Error as err:
            print(f"Error fetching leaderboard content: {err}")
        return leaderboard_data

