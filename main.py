from fastapi import FastAPI
import endpoints
from database import Base, engine
import tables

app = FastAPI()
app.include_router(endpoints.router)

Base.metadata.create_all(bind=engine)
