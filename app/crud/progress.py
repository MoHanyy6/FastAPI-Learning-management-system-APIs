from sqlalchemy.orm import Session
from app import models, schemas

def mark_lesson_completed(db: Session, user_id: int, lesson_id: int):
    progress = db.query(models.Progress).filter(
        models.Progress.user_id == user_id,
        models.Progress.lesson_id == lesson_id
    ).first()

    if not progress:
        progress = models.Progress(user_id=user_id, lesson_id=lesson_id, completed=True)
        db.add(progress)
    else:
        progress.completed = True

    db.commit()
    db.refresh(progress)
    return progress

def get_progress_by_user(db: Session, user_id: int):
    return db.query(models.Progress).filter(models.Progress.user_id == user_id).all()
