from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional

class ExerciseCreate(BaseModel):
    name: str

class ExerciseReturned(BaseModel):
    id: int
    name: str

class SetsCreate(BaseModel):
    exercise_id: int
    rpe: Optional[int] = Field(ge=6, le=10)
    set: int
    reps: int
    weight: float



class SetsReturned(BaseModel):
    id: int
    sets: int 

class SessionCreate(BaseModel):
    user_id: int
    date: date
    notes: Optional[str] = None

class SessionRead(BaseModel):
    id: int
    user_id: int
    date: date
    created_at: datetime
    notes: Optional[str]

class OneRMCreate(BaseModel):
    date: date
    id: int
    notes: Optional[str]
    exercise_id: int
    