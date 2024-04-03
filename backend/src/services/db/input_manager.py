from src.services.db.manager import DatabaseManager
from src.models.input_model import InputModel

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
    
    def add_score(self, score, id):
        query = "UPDATE input SET score = score + %s WHERE id = %s"
        update = self.cursor.execute(query, (score, id))
        return update
    
    def add_numberof(self, numberOfPeople,numberOfEngagedPeople, id):
        query = "UPDATE input SET numberOfPeople = numberOfPeople + %s, numberOfEngagedPeople = numberOfEngagedPeople + %s WHERE id = %s"
        update2 = self.cursor.execute(query, (numberOfPeople, numberOfEngagedPeople, id))
        return update2

    def get_initial_data(self):
        query = "SELECT * FROM input"
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        return data
        