from fastapi import FastAPI
from app.api.routes import notes, paper
from app.db.database import Base, engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(notes.router, prefix="/notes", tags=["Notes"])
app.include_router(paper.router, prefix="/paper", tags=["Paper"])
