from sqlalchemy.orm import Session
from app import models, schemas

def enroll_student(db: Session, enrollment: schemas.EnrollmentCreate):
    db_enrollment = models.Enrollment(
        user_id=enrollment.user_id,
        course_id=enrollment.course_id,
        progress=0
    )
    db.add(db_enrollment)
    db.commit()
    db.refresh(db_enrollment)
    return db_enrollment

def get_enrollments(db: Session, user_id: int = None, course_id: int = None):
    query = db.query(models.Enrollment)
    if user_id:
        query = query.filter(models.Enrollment.user_id == user_id)
    if course_id:
        query = query.filter(models.Enrollment.course_id == course_id)
    return query.all()

def delete_enrollment(db: Session, enrollment_id: int):
    enrollment = db.query(models.Enrollment).filter(models.Enrollment.id == enrollment_id).first()
    if not enrollment:
        return None
    db.delete(enrollment)
    db.commit()
    return enrollment
