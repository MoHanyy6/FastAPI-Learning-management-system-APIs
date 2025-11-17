# crud/quizzes.py
from sqlalchemy.orm import Session
from app import models, schemas
from..crud import quizzes,questions

def create_quiz(db: Session, course_id: int, quiz: schemas.QuizCreate):
    db_quiz = models.Quiz(title=quiz.title, course_id=course_id)
    db.add(db_quiz)
    db.commit()
    db.refresh(db_quiz)

    for q in quiz.questions:
        db_question = models.Question(
            quiz_id=db_quiz.id,
            question_text=q.question_text,
            options=q.options,
            correct_option=q.correct_option
        )
        db.add(db_question)
    db.commit()
    return db_quiz

def get_quizzes_by_course(db: Session, course_id: int):
    return db.query(models.Quiz).filter(models.Quiz.course_id == course_id).all()

def get_quiz(db: Session, quiz_id: int):
    return db.query(models.Quiz).filter(models.Quiz.id == quiz_id).first()

def update_quiz(db: Session, quiz_id: int, quiz: schemas.QuizUpdate):
    db_quiz = get_quiz(db, quiz_id)
    if not db_quiz:
        return None
    if quiz.title:
        db_quiz.title = quiz.title
    db.commit()
    db.refresh(db_quiz)
    return db_quiz

def delete_quiz(db: Session, quiz_id: int):
    db_quiz = get_quiz(db, quiz_id)
    if not db_quiz:
        return None
    db.delete(db_quiz)
    db.commit()
    return db_quiz
