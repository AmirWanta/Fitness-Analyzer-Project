from pydantic import BaseModel, Field, EmailStr
from datetime import datetime, date
from typing import Optional

class ExerciseCreate(BaseModel):
    name: str

class ExerciseRead(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}


class SetCreate(BaseModel):
    exercise_id: int
    rpe: Optional[float] = Field(None, ge=6, le=10)
    reps: int
    weight: float
    is_top_set: Optional[bool] = None

class SetRead(BaseModel):
    id: int
    session_id: int
    exercise_id: int
    reps: int
    rpe: Optional[float]
    is_top_set: bool
    created_at: datetime
    weight: float

    model_config = {"from_attributes": True}

class SetUpdate(BaseModel):
    rpe: Optional[float] = Field(None, ge=6, le=10)
    reps: Optional[int] = None
    weight: Optional[float] = None
    is_top_set: Optional[bool] = None

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

    model_config = {"from_attributes": True}



class UserCreate(BaseModel):
    email: EmailStr
    password: str
    unit: str
    training_mode: str

class UserRead(BaseModel):
    id: int
    email: EmailStr
    unit: str
    training_mode: str
    created_at: datetime

    model_config = {"from_attributes": True}

class LoginInfo(BaseModel):
    email: EmailStr
    password: str

class OneRmRead(BaseModel):
    weight: float
    reps: int
    estimated_1rm: float