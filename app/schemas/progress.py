from pydantic import BaseModel

class ProgressCreate(BaseModel):
    user_id: int
    lesson_id: int
    completed: bool = False

class ProgressUpdate(BaseModel):
    completed: bool

class ProgressResponse(BaseModel):
    id: int
    user_id: int
    lesson_id: int
    completed: bool

    class Config:
        orm_mode = True