from pydantic  import BaseModel,EmailStr
from pydantic.types import conint
from datetime import datetime, timezone
from typing import Optional,List


class LessonCreate(BaseModel):
    title: str
    content: str
    video_url: Optional[str] = None
    order: int

# Response schema for a lesson
class LessonResponse(LessonCreate):
    id: int
    course_id: int

    class Config:
        orm_mode = True

# Optional bulk creation schema
class LessonBulkCreate(BaseModel):
    lessons: List[LessonCreate]