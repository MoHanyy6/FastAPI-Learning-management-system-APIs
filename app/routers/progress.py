from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import crud, schemas
from app.database import get_db
from ..crud import progress as crud_progress  # alias to avoid name clash
router = APIRouter(
    prefix="/progress",
    tags=["Progress"]
)

@router.post("/", response_model=schemas.ProgressResponse)
def mark_completed(progress: schemas.ProgressCreate, db: Session = Depends(get_db)):
    return crud_progress.mark_lesson_completed(db, progress.user_id, progress.lesson_id)

@router.get("/user/{user_id}", response_model=List[schemas.ProgressResponse])
def get_user_progress(user_id: int, db: Session = Depends(get_db)):
    return crud_progress.get_progress_by_user(db, user_id)
