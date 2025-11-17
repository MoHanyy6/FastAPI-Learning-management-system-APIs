from fastapi import FastAPI , Query, Path,Body,status,HTTPException,Depends,APIRouter,Request
from typing import List
from .. import models,schemas,utils,dependencies,oauth2
from sqlalchemy.orm import Session
from ..database import engine,get_db
from..crud import users,courses,lessons





router=APIRouter(
    prefix="/courses"
    ,
    tags=['Courses']
)

@router.get("/", response_model=List[schemas.CourseResponse])
def get_courses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),current_user: models.User = Depends(oauth2.get_current_user)):
    return courses.get_courses(db, skip=skip, limit=limit)


@router.post("/", response_model=schemas.CourseCreate, status_code=status.HTTP_201_CREATED)

def create_new_course(course: schemas.CourseCreate, db: Session = Depends(get_db),current_user: models.User = Depends(dependencies.require_role("admin")),request: Request = None):
    
    return courses.create_course(course,db)

@router.get("/{course_id}", response_model=schemas.CourseResponse)
def read_course(course_id:int,skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return courses.get_course(course_id,db, skip=skip, limit=limit)


@router.put("/{course_id}", response_model=schemas.CourseCreate)
def new_course(course_id:int,course:schemas.CourseCreate, db: Session = Depends(get_db),current_user: models.User = Depends(dependencies.require_role("admin"))):
    return courses.update_course(course_id,course,db)



# Create ONE lesson
@router.post("/{course_id}/lessons", response_model=schemas.LessonResponse)
def create_lesson(course_id: int, payload: schemas.LessonCreate, db: Session = Depends(get_db),current_user: models.User = Depends(dependencies.require_role("instructor"))):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return lessons.create_lesson(db, course_id, payload)


# Create MULTIPLE lessons for admin only
@router.post("/{course_id}/lessons/bulk", response_model=list[schemas.LessonResponse])
def create_lessons_bulk(course_id: int, payload: schemas.LessonBulkCreate, db: Session = Depends(get_db),current_user: models.User = Depends(dependencies.require_role("instructor"))):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return lessons.create_lessons_bulk(db, course_id, payload.lessons)