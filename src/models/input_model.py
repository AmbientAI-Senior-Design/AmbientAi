from pydantic import BaseModel


class InputModel(BaseModel):
    image_score: int
    input_name: str
    input_image_path: str
    client_name: str
