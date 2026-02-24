from datetime import date
from uuid import UUID

from pydantic import BaseModel, Field


class ExamCreate(BaseModel):
    subject_id: UUID
    title: str = Field(min_length=1, max_length=200)
    exam_date: date
    target_hours: int = Field(ge=1, le=1000)
    priority: int = Field(ge=1, le=5)


class ExamUpdate(BaseModel):
    subject_id: UUID
    title: str = Field(min_length=1, max_length=200)
    exam_date: date
    target_hours: int = Field(ge=1, le=1000)
    priority: int = Field(ge=1, le=5)
