from src.services.db.manager import DatabaseManager
from src.models.input_model import PostModel, EngagementReportModel, SlideModel, BackendModel
class InputManager(DatabaseManager):

    def __init__(self):
        super().__init__("ClientInput")


    def get_id(self):
        model : PostModel
        self.cursor.execute("INSERT INTO Post VALUES ();")
        self._conn.commit()
        self.cursor.execute("SELECT LAST_INSERT_ID();")
        post_id = self.cursor.fetchone()[0]
        return post_id

    def add_new_row_to_Post(self):
        self.cursor.execute("INSERT INTO Post () VALUES ();")
        self._conn.commit()
        return self.get_id()

    def add_slide(self, slide: SlideModel):
        query = "INSERT INTO Slide (path, description, fk_post_id, slide_index) VALUES (%s, %s, %s, %s)"
        values = (slide.path, slide.description, slide.fk_post_id, slide.slide_index)
        self.cursor.execute(query, values)
        self._conn.commit()

    def populate_db(self, data):
        model = EngagementReportModel(**data)
        pid = data['pid']
        post_id = self.get_id()
        query = " INSERT INTO EngagementReport (id, date, duration, numberOfPeople, numberOfEngagedPeople, score, fk_post_id, slide_index) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        params = (model.id, model.date, model.duration, model.numberOfPeople, model.numberOfEngagedPeople, model.score, model.fk_post_id, model.slide_index)
        self.cursor.execute(query,params)
        self._conn.commit()

    def get_all_slides(self):
        self.cursor.execute("SELECT path, description FROM Slide")
        slides = self.cursor.fetchall()
        return slides

#    def leaderboard_db(self):


    
    #def leaderboard_data(self, model: EngagementReportModel): # gathers data for leaderboard.html
    #    query = "SELECT client_name, score FROM PostModel ORDER BY score DESC"
    #    self.cursor.execute(query)
    #    data = self.cursor.fetchall()
    #    return data


    #def create_input(self, model: EngagementReportModel):