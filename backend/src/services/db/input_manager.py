from src.services.db.manager import DatabaseManager
from src.models.input_model import PostModel, EngagementReportModel, SlideModel, BackendModel

# a get request


class InputManager(DatabaseManager):


    def __init__(self):
        super().__init__("ClientInput")


    def get_id(self):
        model : PostModel
        self.cursor.execute("INSERT INTO Post VALUES ();")# make new row
        self.connection.commit()
        self.cursor.execute("SELECT LAST_INSERT_ID();") # get last id
        post_id = self.cursor.fetchone()[0]
        return post_id

    def populate_db(self, data):
        model = EngagementReportModel(**data)
        pid = data['pid']
        if model.fk_post_id is None:
            post_id = self.get_id()
            query = " INSERT INTO EngagementReport (id, date, duration, numberOfPeople, numberOfEngagedPeople, score, fk_post_id, slide_index) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            params = (model.id, model.date, model.duration, model.numberOfPeople, model.numberOfEngagedPeople, model.score, model.fk_post_id, model.slide_index)
            self.cursor.execute(query,params)
            self.connection.commit()



    
    #def leaderboard_data(self, model: EngagementReportModel): # gathers data for leaderboard.html
    #    query = "SELECT client_name, score FROM PostModel ORDER BY score DESC"
    #    self.cursor.execute(query)
    #    data = self.cursor.fetchall()
    #    return data


    #def create_input(self, model: EngagementReportModel):