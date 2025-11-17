from pydantic  import BaseModel,EmailStr
from pydantic.types import conint
from datetime import datetime, timezone
from typing import Optional,List




class CourseBase(BaseModel):
    title: str
    description: str
    instructor_id: int

class CourseCreate(CourseBase):
    pass

class CourseResponse(CourseBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True  