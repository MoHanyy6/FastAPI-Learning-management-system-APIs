from fastapi import FastAPI , Query, Path,Body,status,HTTPException,Depends,Request
from typing import List
from random import randrange

from . import models,schemas,utils,crud
from sqlalchemy.orm import Session
from .database import engine,get_db
from .routers import users,courses,quizzes,questions,enrollment,progress,auth








models.Base.metadata.create_all(bind=engine)
print("✅ Tables should now be created if they don’t exist.")

app = FastAPI()

# app.state.limiter = limiter
# app.add_middleware(SlowAPIMiddleware)

app.include_router(auth.router, prefix="/auth")
app.include_router(users.router)
app.include_router(courses.router)
app.include_router(quizzes.router)
app.include_router(questions.router)
app.include_router(enrollment.router)
app.include_router(progress.router)




@app.get("/")
async def home():
   return {"key": "value"}





