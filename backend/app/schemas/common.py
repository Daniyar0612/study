from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class SubjectOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str


class ExamOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    subject_id: UUID
    title: str
    exam_date: date
    target_hours: int
    priority: int


class PlanItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    exam_id: UUID
    date: date
    hours: float
    status: str
