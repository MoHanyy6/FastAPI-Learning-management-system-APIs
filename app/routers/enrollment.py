from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import crud, schemas
from app.database import get_db
from..crud import enrollment
from .. import dependencies,models,oauth2

router = APIRouter(
    prefix="/enrollments",
    tags=["Enrollments"]
)

@router.post("/", response_model=schemas.EnrollmentResponse)
def enroll_student(enrollment: schemas.EnrollmentCreate, db: Session = Depends(get_db)):
    return crud.enrollment.enroll_student(db, enrollment)

@router.get("/", response_model=List[schemas.EnrollmentResponse])
def list_enrollments(user_id: int = None, course_id: int = None, db: Session = Depends(get_db),
                     current_user: models.User = Depends(oauth2.get_current_user)):
    
    if current_user.role != "admin":
        user_id = current_user.id

    return enrollment.get_enrollments(db, user_id, course_id)

@router.delete("/{enrollment_id}")
def delete_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
    enrollment = enrollment.delete_enrollment(db, enrollment_id)
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    return {"detail": "Enrollment deleted"}
