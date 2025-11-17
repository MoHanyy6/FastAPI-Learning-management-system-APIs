from fastapi import FastAPI , Query, Path,Body,status,HTTPException,Depends,APIRouter
from typing import List
from .. import models,schemas,utils,dependencies
from sqlalchemy.orm import Session
from ..database import engine,get_db
from..crud import users

router=APIRouter(
    prefix="/users"
    ,
    tags=['Users']
)
@router.get("/", response_model=List[schemas.UserResponse])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),current_user: models.User = Depends(dependencies.require_role("admin"))):
    return users.get_users(db, skip=skip, limit=limit)


@router.get("/by_email", response_model=schemas.UserResponse)
def get_user_by_email(
    user_email: str = Query(..., description="Email of the user to fetch"),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(dependencies.require_role("admin"))
):
    user = users.get_user_by_email(user_email, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The user with email {user_email} was not found"
        )
    return user

@router.get("/{user_id}",response_model=schemas.UserResponse)
def get_user(user_id:int, db: Session = Depends(get_db),current_user: models.User = Depends(dependencies.require_role("admin"))):
    user=users.get_user_by_id(user_id,db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"the user with id {user_id} is not found")
    return user

# Create User
@router.post("/", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def create_new_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = users.get_user_by_email(user.email, db)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return users.create_user(user, db)


# Update User
@router.put("/{user_id}", response_model=schemas.UserResponse)
def update_existing_user(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db),current_user: models.User = Depends(dependencies.require_role("admin"))):
    updated_user = users.update_user(user_id, user, db)
    if not updated_user:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
    return updated_user
