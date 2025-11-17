# crud/questions.py
from sqlalchemy.orm import Session
from app import models, schemas

def create_question(db: Session, quiz_id: int, question: schemas.QuestionCreate):
    db_question = models.Question(
        quiz_id=quiz_id,
        question_text=question.question_text,
        options=question.options,
        correct_option=question.correct_option
    )
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

def get_question(db: Session, question_id: int):
    return db.query(models.Question).filter(models.Question.id == question_id).first()

def update_question(db: Session, question_id: int, question: schemas.QuestionUpdate):
    db_question = get_question(db, question_id)
    if not db_question:
        return None
    if question.question_text:
        db_question.question_text = question.question_text
    if question.options:
        db_question.options = question.options
    if question.correct_option:
        db_question.correct_option = question.correct_option
    db.commit()
    db.refresh(db_question)
    return db_question

def delete_question(db: Session, question_id: int):
    db_question = get_question(db, question_id)
    if not db_question:
        return None
    db.delete(db_question)
    db.commit()
    return db_question
