# routers/questions.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import crud, schemas
from app.database import get_db
from .. import dependencies
router = APIRouter(
    prefix="/questions",
    tags=["Questions"],
    dependencies=[Depends(dependencies.require_role("instructor"))]
)

@router.post("/quiz/{quiz_id}", response_model=schemas.QuestionResponse)
def create_question(quiz_id: int, question: schemas.QuestionCreate, db: Session = Depends(get_db)):
    return crud.questions.create_question(db, quiz_id, question)

@router.get("/{question_id}", response_model=schemas.QuestionResponse)
def get_question(question_id: int, db: Session = Depends(get_db)):
    db_question = crud.questions.get_question(db, question_id)
    if not db_question:
        raise HTTPException(status_code=404, detail="Question not found")
    return db_question

@router.put("/{question_id}", response_model=schemas.QuestionResponse)
def update_question(question_id: int, question: schemas.QuestionUpdate, db: Session = Depends(get_db)):
    db_question = crud.questions.update_question(db, question_id, question)
    if not db_question:
        raise HTTPException(status_code=404, detail="Question not found")
    return db_question

@router.delete("/{question_id}")
def delete_question(question_id: int, db: Session = Depends(get_db)):
    db_question = crud.questions.delete_question(db, question_id)
    if not db_question:
        raise HTTPException(status_code=404, detail="Question not found")
    return {"detail": "Question deleted"}
