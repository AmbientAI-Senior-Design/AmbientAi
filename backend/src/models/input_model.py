from pydantic import BaseModel, Field
from typing import List, Optional, Text
from datetime import date

class InputModel(BaseModel):
    date: Optional[str] = Field(None)
    duration: Optional[int] = Field(None)
    numberOfPeople: Optional[int] = Field(None)
    numberOfEngagedPeople: Optional[int] = Field(None)
    score: Optional[int] = Field(None)
    slideId: Optional[int] = Field(None)
    image_data: Optional[str] = Field(None)

class PostModel(BaseModel):
    id: Optional[int] = None  

class EngagementReportModel(BaseModel):
    id: Optional[int] = None  
    date: date
    duration: int
    numberOfPeople: int
    numberOfEngagedPeople: int
    score: float
    fk_post_id: int

class SlideModel(BaseModel):
    id: Optional[int] = None  
    path: str
    description: Text
    fk_post_id: int
    slide_index: int

class BackendModel(BaseModel):
    image_name: str
    score: int


