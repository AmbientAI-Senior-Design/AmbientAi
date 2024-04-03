from pydantic import BaseModel


class InputModel(BaseModel):
    input_id: str
    image_score: int
    input_name: str
    input_image_path: str
    client_name: str
