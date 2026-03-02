from fastapi import FastAPI
from endpoints import router
from database import Base, engine
import tables

app = FastAPI()
app.include_router(router)

Base.metadata.create_all(bind=engine)