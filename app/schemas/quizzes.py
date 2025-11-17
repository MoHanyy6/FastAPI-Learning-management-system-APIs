from pydantic  import BaseModel,EmailStr
from pydantic.types import conint
from datetime import datetime, timezone
from typing import Optional,List
from .questions import QuestionCreate,QuestionResponse



class QuizCreate(BaseModel):
    title: str
    questions: List[QuestionCreate] = []

class QuizUpdate(BaseModel):
    title: Optional[str]

class QuizResponse(BaseModel):
    id: int
    title: str
    course_id: int
    questions: List[QuestionResponse] = []

    class Config:
        orm_mode = True