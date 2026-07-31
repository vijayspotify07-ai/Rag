from fastapi import FastAPI

from app.db import engine

from app.db import Base

from app.routers import jobs

from app.routers import candidates


Base.metadata.create_all(

    bind=engine
)


app = FastAPI(

    title="Recruit-RAG API",

    description="AI Recruitment System",

    version="1.0.0"
)


app.include_router(

    jobs.router
)


app.include_router(

    candidates.router
)


@app.get("/")
def home():

    return {

        "message": "Recruit-RAG API is running"
    }