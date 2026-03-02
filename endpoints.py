from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from tables import Exercise
from schemas import ExerciseCreate, ExerciseRead

router = APIRouter()

@router.post("/exercises", response_model=ExerciseRead)
def create_Exercise(payload: ExerciseCreate, db: Session = Depends(get_db)):
    db_exercise = Exercise(name=payload.name)
    
    db.add(db_exercise)
    db.commit()
    db.refresh(payload)
    
    return db_exercise

@router.get("/exercises", response_model=list[ExerciseRead])
def get_exercises(db: Session = Depends(get_db)):
    exercises = db.query(Exercise).all()
    return exercises

