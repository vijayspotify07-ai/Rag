from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import Float
from sqlalchemy import ForeignKey

from app.db import Base


class Job(Base):

    __tablename__ = "jobs"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    title = Column(
        String(255),
        nullable=False
    )

    description = Column(
        Text,
        nullable=False
    )

    requirements = Column(
        Text,
        nullable=True
    )


class Candidate(Base):

    __tablename__ = "candidates"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String(255),
        nullable=False
    )

    email = Column(
        String(255),
        nullable=True
    )

    resume_text = Column(
        Text,
        nullable=False
    )

    resume_filename = Column(
        String(255),
        nullable=True
    )


class Score(Base):

    __tablename__ = "scores"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    job_id = Column(
        Integer,
        ForeignKey("jobs.id")
    )

    candidate_id = Column(
        Integer,
        ForeignKey("candidates.id")
    )

    score = Column(
        Float
    )

    explanation = Column(
        Text
    )