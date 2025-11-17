from sqlalchemy.orm import Session
from .. import models, schemas

def create_lesson(db: Session, course_id: int, lesson: schemas.LessonCreate):
    db_lesson = models.Lesson(
        title=lesson.title,
        content=lesson.content,
        video_url=lesson.video_url,
        order=lesson.order,
        course_id=course_id
    )
    db.add(db_lesson)
    db.commit()
    db.refresh(db_lesson)
    return db_lesson

def create_lessons_bulk(db: Session, course_id: int, lessons: list[schemas.LessonCreate]):
    created = []
    for lesson in lessons:
        new_lesson = models.Lesson(
            title=lesson.title,
            content=lesson.content,
            video_url=lesson.video_url,
            order=lesson.order,
            course_id=course_id
        )
        db.add(new_lesson)
        created.append(new_lesson)
    db.commit()
    for l in created:
        db.refresh(l)
    return created
