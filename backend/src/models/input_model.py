from pydantic import BaseModel
from typing import List, Optional, Text
from datetime import date

class PostModel(BaseModel):
    id: Optional[int] = None  

class EngagementReportModel(BaseModel):
    id: Optional[int] = None
    date: Optional[date] = None
    duration: Optional[int] = None
    numberOfPeople: Optional[int] = None
    numberOfEngagedPeople: Optional[int] = None
    score: Optional [float]  
    fk_post_id: Optional[int] = None
    slide_index: Optional[int] = None

class SlideModel(BaseModel):
    id: Optional[int] = None  
    path: str
    description: Text
    fk_post_id: int
    slide_index: int

class BackendModel(BaseModel):
    image_name: str
    score: int


