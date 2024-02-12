from pydantic import BaseModel


class LeaderBoard(BaseModel):
    image_score: int
    input_name: str
    input_image_path: str
    client_name: str
