from fastapi import FastAPI, HTTPException, APIRouter

router = APIRouter()

@router.get("/test")
def test():
    return "Hi"