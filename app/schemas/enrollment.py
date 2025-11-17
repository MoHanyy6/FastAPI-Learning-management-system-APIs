# schemas/enrollment.py
from pydantic import BaseModel
from typing import List, Optional

class EnrollmentCreate(BaseModel):
    user_id: int
    course_id: int

class EnrollmentResponse(BaseModel):
    id: int
    user_id: int
    course_id: int
    progress: int

    class Config:
        orm_mode = True
