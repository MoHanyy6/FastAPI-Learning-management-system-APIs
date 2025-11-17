# routers/quizzes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import crud, schemas
from app.database import get_db
from..crud import quizzes,questions
from.. import dependencies

router = APIRouter(
    prefix="/quizzes",
    tags=["Quizzes"],
    dependencies=[Depends(dependencies.require_role("instructor"))]
)

@router.post("/course/{course_id}", response_model=schemas.QuizResponse)
def create_quiz(course_id: int, quiz: schemas.QuizCreate, db: Session = Depends(get_db)):
    return quizzes.create_quiz(db, course_id, quiz)

@router.get("/course/{course_id}", response_model=List[schemas.QuizResponse])
def list_quizzes(course_id: int, db: Session = Depends(get_db)):
    return quizzes.get_quizzes_by_course(db, course_id)

@router.get("/{quiz_id}", response_model=schemas.QuizResponse)
def get_quiz(quiz_id: int, db: Session = Depends(get_db)):
    db_quiz = crud.quizzes.get_quiz(db, quiz_id)
    if not db_quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return db_quiz

@router.put("/{quiz_id}", response_model=schemas.QuizResponse)
def update_quiz(quiz_id: int, quiz: schemas.QuizUpdate, db: Session = Depends(get_db)):
    db_quiz = crud.quizzes.update_quiz(db, quiz_id, quiz)
    if not db_quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return db_quiz

@router.delete("/{quiz_id}")
def delete_quiz(quiz_id: int, db: Session = Depends(get_db)):
    db_quiz = crud.quizzes.delete_quiz(db, quiz_id)
    if not db_quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return {"detail": "Quiz deleted"}
