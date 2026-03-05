from database import Base
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Date, Float, Boolean, CheckConstraint


class Exercise(Base):
    __tablename__ = "exercises"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    unit = Column(String(2), nullable=False, default="lb")
    training_mode = Column(String(32), nullable=False, default="powerlifting")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

class Session(Base):                 
    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(Date, nullable=False)
    notes= Column(String(255), nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

class Set(Base):
    __tablename__ = "sets"
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)
    exercise_id = Column(Integer, ForeignKey("exercises.id"), nullable=False)
    reps = Column(Integer, nullable=False)
    weight = Column(Float , nullable=False)
    is_top_set = Column(Boolean, nullable=False, default=False)
    rpe = Column(Float, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    __table_args__ = (
        CheckConstraint("weight > 0", name="check_weight_positive"),
        CheckConstraint("reps > 0", name="check_positive_reps"),
        CheckConstraint("rpe >= 6 AND rpe <= 10", name="check_rpe_range"),
    
    )
