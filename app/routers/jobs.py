from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.db import get_db

from app.models import Job
from app.models import Candidate
from app.models import Score

from app.schemas import JobCreate

from app.services.scorer import score_candidate


router = APIRouter(

    prefix="/jobs",

    tags=["Jobs"]

)


@router.post("/")
def create_job(

    job_data: JobCreate,

    db: Session = Depends(get_db)

):

    job = Job(

        title=job_data.title,

        description=job_data.description

    )


    db.add(job)

    db.commit()

    db.refresh(job)


    return job


@router.get("/")
def get_jobs(

    db: Session = Depends(get_db)

):

    return db.query(Job).all()


@router.get("/{job_id}")
def get_job(

    job_id: int,

    db: Session = Depends(get_db)

):

    job = (

        db.query(Job)

        .filter(Job.id == job_id)

        .first()

    )


    if not job:

        raise HTTPException(

            status_code=404,

            detail="Job not found"

        )


    return job


@router.post(

    "/{job_id}/candidates/{candidate_id}/score"

)

def score_candidate_for_job(

    job_id: int,

    candidate_id: int,

    db: Session = Depends(get_db)

):

    
    # 1. Find the job
    

    job = (

        db.query(Job)

        .filter(Job.id == job_id)

        .first()

    )


    if not job:

        raise HTTPException(

            status_code=404,

            detail="Job not found"

        )


    
    # 2. Find the candidate
    

    candidate = (

        db.query(Candidate)

        .filter(Candidate.id == candidate_id)

        .first()

    )


    if not candidate:

        raise HTTPException(

            status_code=404,

            detail="Candidate not found"

        )


    
    # 3. Call OpenAI
    

    try:

        result = score_candidate(

            job_description=job.description,

            resume_text=candidate.resume_text

        )


    except Exception as error:

        raise HTTPException(

            status_code=503,

            detail=str(error)

        )



    # 4. Save result in MySQL


    score = Score(

        job_id=job.id,

        candidate_id=candidate.id,

        score=result["score"],

        explanation=result["explanation"]

    )


    db.add(score)

    db.commit()

    db.refresh(score)


    
    # 5. Return result
    

    return {

        "message": "Candidate scored successfully",

        "job_id": job.id,

        "candidate_id": candidate.id,

        "score": result["score"],

        "matched_skills": result["matched_skills"],

        "missing_skills": result["missing_skills"],

        "explanation": result["explanation"]

    }
