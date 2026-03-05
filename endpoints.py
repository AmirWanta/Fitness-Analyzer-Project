from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from tables import *
from schemas import ExerciseCreate, ExerciseRead, UserCreate, UserRead

router = APIRouter()

@router.post("/exercises", response_model=ExerciseRead)
def create_Exercise(payload: ExerciseCreate, db: Session = Depends(get_db)):
    db_exercise = Exercise(name=payload.name)
    
    db.add(db_exercise)
    db.commit()
    db.refresh(db_exercise)
    
    return db_exercise

@router.get("/exercises", response_model=list[ExerciseRead])
def get_exercises(db: Session = Depends(get_db)):
    exercises = db.query(Exercise).all()
    return exercises

@router.post("/users", response_model=UserRead)
def create_User(payload: UserCreate, db: Session = Depends(get_db)):
    new_User = User (
        email = payload.email,
        password = payload.password,
        unit = payload.unit,
        training_mode = payload.training_mode
    )

    db.add(new_User)
    db.commit()
    db.refresh(new_User)

    return new_User

@router.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
       raise HTTPException(status_code=404, detail="User not found")

    return user