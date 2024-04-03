from src.services.db.manager import DatabaseManager
from src.models.input_model import PostModel, EngagementReportModel, SlideModel, BackendModel

# a get request


class InputManager(DatabaseManager):


    def __init__(self):
        super().__init__("ClientInput")
    
    def leaderboard_data(self): # gathers data for leaderboard.html
        query = "SELECT client_name, score FROM backend ORDER BY score DESC"
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        return data


    def create_input(self, model: InputModel):
        query = """
        INSERT INTO input (date, duration, numberOfPeople, numberOfEngagedPeople, score, slideId, image_data)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            model.date,
            model.duration,
            model.numberOfPeople,
            model.numberOfEngagedPeople,
            model.score,
            model.image_data 
        )
        res = self.cursor.execute(query, params)
        return res

        