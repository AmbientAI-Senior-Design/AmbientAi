from pydantic import BaseModel
from typing import List

class ImageData(BaseModel):
    filename: str
    description: str

class ImageDataStructure(BaseModel):
    main_image: ImageData
    related_images: List[ImageData]

class InputModel(BaseModel):
    id: int
    date: str
    duration: str
    numberOfPeople: int
    numberOfEngagedPeople: int
    score: float
    image_data: ImageDataStructure

class backendmodel(BaseModel):
    image_name: str
    score: int


