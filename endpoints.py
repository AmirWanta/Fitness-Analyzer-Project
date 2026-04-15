from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as DBSession
from sqlalchemy.exc import IntegrityError

from security import *
from database import get_db
from tables import Session as WorkoutSession, User, Exercise, Set
from schemas import *

router = APIRouter()

@router.post("/exercises", response_model=ExerciseRead)
def create_Exercise(payload: ExerciseCreate, db: DBSession = Depends(get_db), user_id: int = Depends(get_current_user)):
    db_exercise = Exercise(name=payload.name)
    
    db.add(db_exercise)
    db.commit()
    db.refresh(db_exercise)
    
    return db_exercise


@router.get("/exercises", response_model=list[ExerciseRead])
def get_exercises(db: DBSession = Depends(get_db)):
    exercises = db.query(Exercise).all()
    return exercises


@router.post("/users", response_model=UserRead)
def create_User(payload: UserCreate, db: DBSession = Depends(get_db)):

    hashed = hashPassword(payload.password)

    new_User = User (
        email = payload.email,
        password = hashed,
        unit = payload.unit,
        training_mode = payload.training_mode
    )
    
    
    db.add(new_User)
    
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Email already registered")

    db.refresh(new_User)

    return new_User


@router.get("/users/{user_id}", response_model=UserRead)
def get_user(user_id: int, db: DBSession = Depends(get_db), current_user: int = Depends(get_current_user)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
       raise HTTPException(status_code=404, detail="User not found")

    return user


@router.post("/sessions", response_model=SessionRead)
def create_session(payload: SessionCreate, db: DBSession = Depends(get_db), user_id: int = Depends(get_current_user)):
    user = db.query(User).filter(User.id == payload.user_id).first()

    if not user:
       raise HTTPException(status_code=404, detail="User not found")

    newSession = WorkoutSession (
        user_id = payload.user_id,
        date = payload.date,
        notes = payload.notes,
    )

    db.add(newSession)
    db.commit()
    db.refresh(newSession)
    
    return newSession


@router.post("/sessions/{session_id}/sets", response_model=SetRead)
def addSets(payload: SetCreate, session_id: int, db: DBSession = Depends(get_db), user_id: int = Depends(get_current_user)):

    session = db.query(WorkoutSession).filter(WorkoutSession.id == session_id).first()

    if not session: 
       raise HTTPException(status_code=404, detail="Session not found")

    newSet = Set (
        session_id = session_id,
        exercise_id = payload.exercise_id,
        rpe = payload.rpe,
        reps = payload.reps,
        weight = payload.weight,
        is_top_set = payload.is_top_set
    )

    
    db.add(newSet)
    db.commit()
    db.refresh(newSet)

    return newSet


@router.get("/sessions/{session_id}", response_model=SessionRead)
def getSession(session_id: int, db: DBSession = Depends(get_db), user_id: int = Depends(get_current_user)):
    session = db.query(WorkoutSession).filter(WorkoutSession.id == session_id).first()

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return session


@router.delete("/sessions/{session_id}", status_code=204)
def deleteSession(session_id: int, db: DBSession = Depends(get_db), user_id: int = Depends(get_current_user)):

    sessionDelete = db.get(WorkoutSession, session_id)

    if not sessionDelete:
        raise HTTPException(status_code=404, detail="Session not found")
    
    db.delete(sessionDelete)
    db.commit()


@router.delete("/sessions/{session_id}/sets/{set_id}", status_code=204)
def deleteSet(session_id: int, set_id: int, db: DBSession = Depends(get_db), user_id: int = Depends(get_current_user)):

    setDelete = db.get(Set, set_id)

    if not setDelete:
        raise HTTPException(status_code=404, detail="Set not found")

    db.delete(setDelete)
    db.commit()


@router.patch("/sessions/{session_id}/sets/{set_id}", response_model=SetRead)
def updateSets(payload: SetUpdate, session_id: int, set_id: int, db: DBSession = Depends(get_db), user_id: int = Depends(get_current_user)):

    setToUpdate = db.get(Set, set_id)

    if not setToUpdate:
        raise HTTPException(status_code=404, detail="Set not found")
    
    updatedSet = payload.model_dump(exclude_unset=True)

    for key, value in updatedSet.items():
        setattr(setToUpdate, key, value)

    db.add(setToUpdate)
    db.commit()
    db.refresh(setToUpdate)

    return setToUpdate


@router.get("/users/{user_id}/sessions", response_model=list[SessionRead])
def getAllSessions(user_id: int, db: DBSession = Depends(get_db), current_user: int = Depends(get_current_user)):
    
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
       raise HTTPException(status_code=404, detail="User not found")

    allSessions = db.query(WorkoutSession).filter(WorkoutSession.user_id == user_id).all()

    return allSessions


@router.get("/sessions/{session_id}/sets", response_model=list[SetRead])
def getAllSets(session_id: int, db: DBSession = Depends(get_db), user_id: int = Depends(get_current_user)):

    session = db.query(WorkoutSession).filter(WorkoutSession.id == session_id).first()

    if not session:
       raise HTTPException(status_code=404, detail="Session not found")
    
    allSets = db.query(Set).filter(Set.session_id == session_id).all()

    return allSets

@router.post("/login")
def login(payload: LoginInfo, db: DBSession = Depends(get_db)):

    user = db.query(User).filter(User.email == payload.email).first()
    
    if not user:
      raise HTTPException(status_code=401, detail="email not found")
  
    
    if not verify_password(payload.password, user.password):
        raise HTTPException(status_code=401, detail="wrong password")

    token = create_token(user.id)

    
    return {"access_token": token}


@router.get("/users/{user_id}/exercises/{exercise_id}/1rm", response_model=OneRmRead)
def oneRmEstimate(user_id: int, exercise_id: int, db: DBSession = Depends(get_db), current_user: int = Depends(get_current_user)):

    userValid = db.query(User).filter(User.id == user_id).first()
    exerciseValid = db.query(Exercise).filter(Exercise.id == exercise_id).first()

    if not userValid:
        raise HTTPException(status_code=404, detail="user not found")
    
    if not exerciseValid:
        raise HTTPException(status_code=404, detail="exercise not found")
    
    sets = db.query(Set).join(WorkoutSession).filter(
    WorkoutSession.user_id == user_id,
    Set.exercise_id == exercise_id
    ).all()

    if not sets:
        raise HTTPException(status_code=404, detail="No sets found for this exercise")
                                
    
    best = None
    for perSet in sets:
        weight = perSet.weight
        reps = perSet.reps

        estimated = perSet.weight * (1 + perSet.reps / 30)
        
        if best is None or estimated > best["estimated_1rm"]:
            best = {"weight": perSet.weight, "reps": perSet.reps, "estimated_1rm": estimated}

    
    return best
    


@router.get("/users/{user_id}/volume")
def totalVolume(user_id: int, current_user: int = Depends(get_current_user), db: DBSession = Depends(get_db)):

    total_volume = 0

    userExist = db.query(User).filter(User.id == user_id).first()

    if not userExist:
        raise HTTPException(status_code=404, detail="User not found")
    
    fullSets = db.query(Set).join(WorkoutSession).filter(
        WorkoutSession.user_id == user_id,
    ).all()

    for perSet in fullSets:
        total_volume += perSet.reps * perSet.weight

    
    return {"total_volume": total_volume}


@router.get("/users/{user_id}/exercise/{exercise_id}/progress")
def progression(
    user_id: int,
    exercise_id: int,
    db: DBSession = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    userExists = db.query(User).filter(User.id == user_id).first()
    exerciseExists = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    
    if not userExists:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not exerciseExists:
        raise HTTPException(status_code=404, detail="Exercise not found")
    
    allSets = (
        db.query(Set, WorkoutSession)
        .join(WorkoutSession, Set.session_id == WorkoutSession.id)
        .filter(
            WorkoutSession.user_id == user_id,
            Set.exercise_id == exercise_id
        )
        .order_by(WorkoutSession.date.asc())
        .all()
    )

    if not allSets:
        raise HTTPException(status_code=404, detail="No sets found for this exercise")

    progress_data = []

    for perSet, perSession in allSets:
        estimated_1rm = perSet.weight * (1 + perSet.reps / 30)

        progress_data.append({
            "date": perSession.date,
            "weight": perSet.weight,
            "reps": perSet.reps,
            "estimated_1rm": round(estimated_1rm, 2)
        })

    return {
        "user_id": user_id,
        "exercise_id": exercise_id,
        "exercise_name": exerciseExists.name,
        "progress": progress_data
    }
    

    
