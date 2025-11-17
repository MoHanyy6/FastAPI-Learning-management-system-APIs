from fastapi import FastAPI , Query, Path,Body,status,HTTPException,Depends,APIRouter
from typing import List,Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from .. import models,schemas,utils,oauth2
from sqlalchemy.orm import Session
from ..database import engine,get_db
from sqlalchemy import func
from..schemas import courses


def get_courses(db: Session ,skip: int = 0, limit: int = 100):
    return db.query(models.Course).offset(skip).limit(limit).all()

def create_course(course: schemas.CourseCreate, db: Session ):
    
    db_course = models.Course(
        title=course.title,
        description=course.description,
        instructor_id=course.instructor_id
    )
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


def get_course(course_id,db: Session ,skip: int = 0, limit: int = 100):
    return db.query(models.Course).filter(models.Course.id==course_id).offset(skip).limit(limit).first()

def update_course(course_id: int, new_data: schemas.CourseCreate,db: Session):
    db_course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not db_course:
        return None
    db_course.title = new_data.title
    db_course.description = new_data.description
    db_course.instructor_id = new_data.instructor_id
    
    db.commit()
    db.refresh(db_course)
    return db_course

# def delete_user(user_id: int,db: Session= Depends(get_db)):
#     db_user = db.query(models.User).filter(models.User.id == user_id).first()
#     if not db_user:
#         return None
#     db.delete(db_user)
#     db.commit()
#     return db_user

def delete_course(course_id:int,db: Session= Depends(get_db)):
    db_course=db.query(models.Course).filter(models.Course.id==course_id).first()
    if not db_course:
        return None
    db.delete(db_course)
    db.commit
    return {"message":"deleted"}
