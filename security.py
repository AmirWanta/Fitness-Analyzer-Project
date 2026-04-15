from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

oauth2_scheme = HTTPBearer()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated ="auto")

SECRET_KEY = "768e575f9c25ec19565e0194089f93fc2af150ecffb439f3b770ac1e9416c48f"

def hashPassword(password):
    result = pwd_context.hash(password)

    return result


def verify_password(plain, hashed):
    result = pwd_context.verify(plain, hashed)

    return result

def create_token(user_id: int):
    

    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(minutes=30)
    }

    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    return encoded_jwt

def verify_token(token: str):

    try:
        decoded_paylod = jwt.decode ( 
            token,
            SECRET_KEY,
            algorithms=["HS256"]
        )
        return decoded_paylod
    
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

def get_current_user(token: str = Depends(oauth2_scheme)):

    result = verify_token(token)

    return result["user_id"]

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    
    token = credentials.credentials
    result = verify_token(token)
    return result["user_id"]