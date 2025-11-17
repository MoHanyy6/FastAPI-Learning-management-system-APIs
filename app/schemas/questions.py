# schemas/question.py
from pydantic import BaseModel
from typing import List, Optional

class QuestionCreate(BaseModel):
    question_text: str
    options: List[str]
    correct_option: str

class QuestionUpdate(BaseModel):
    question_text: Optional[str]
    options: Optional[List[str]]
    correct_option: Optional[str]

class QuestionResponse(BaseModel):
    id: int
    quiz_id: int
    question_text: str
    options: list[str]
    correct_option: str

    class Config:
        orm_mode = True
