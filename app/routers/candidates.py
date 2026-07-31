import os
import shutil

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Form,
    Depends
)

from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Candidate
from app.services.parser import extract_text


router = APIRouter(
    prefix="/candidates",
    tags=["Candidates"]
)


UPLOAD_FOLDER = "uploads"


os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


@router.post("/upload")
def upload_candidate(

    name: str = Form(...),

    email: str = Form(...),

    file: UploadFile = File(...),

    db: Session = Depends(get_db)

):

    file_path = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )


    with open(
        file_path,
        "wb"
    ) as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )


    resume_text = extract_text(
        file_path
    )


    candidate = Candidate(

        name=name,

        email=email,

        resume_text=resume_text,

        resume_filename=file.filename

    )


    db.add(candidate)

    db.commit()

    db.refresh(candidate)


    return {

        "message": "Candidate uploaded successfully",

        "candidate_id": candidate.id,

        "name": candidate.name

    }


@router.get("/")
def get_candidates(

    db: Session = Depends(get_db)

):

    return db.query(Candidate).all()