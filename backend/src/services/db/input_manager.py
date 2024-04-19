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
    
    def add_fk_id(self,fk_id):
        query = "INSERT INTO EngagementReport (fk_post_id) VALUES (%s)"
        query2 = "INSERT INTO Slide (fk_post_id) VALUES (%s)"
        self.cursor.execute(query, (fk_id))
        self._conn.commit()
        self.cursor.execute(query2, (fk_id))
        self._conn.commit()


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

    def insert_into_db(self, data, post_id):
        #model = EngagementReportModel(**data)
        score = data
        print(score)
        last_id = post_id
        print("here")
        print(last_id)
        print("here2")
        if last_id is not None:
            query = "INSERT INTO EngagementReport (score) VALUES (%s)"
            print("here3")
            params = (score,)
        else:
            query = "INSERT INTO EngagementReport (score) VALUES (%s)"
            print("here2")
            params = (score,)
        self.cursor.execute(query, params)
        self._conn.commit()
        print("final")

    def get_all_slides(self):
        self.cursor.execute("SELECT path, description FROM Slide")
        slides = self.cursor.fetchall()
        return slides

    def leaderboard_data(self):
        self.cursor.execute("SELECT fk_post_id, SUM(score) AS total_score FROM EngagementReport GROUP BY fk_post_id ORDER BY total_score DESC;")
        results = self.cursor.fetchall()
        return [{"input_id": row[0], "image_score": row[1]} for row in results]


    
    #def leaderboard_data(self, model: EngagementReportModel): # gathers data for leaderboard.html
    #    query = "SELECT client_name, score FROM PostModel ORDER BY score DESC"
    #    self.cursor.execute(query)
    #    data = self.cursor.fetchall()
    #    return data


    #def create_input(self, model: EngagementReportModel):