from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.exam import Exam
from app.models.subject import Subject
from app.models.user import User
from app.schemas.common import ExamOut
from app.schemas.exam import ExamCreate, ExamUpdate

router = APIRouter(prefix="/exams", tags=["exams"])


def _owned_subject(db: Session, subject_id: UUID, user_id: UUID) -> Subject | None:
    subject = db.get(Subject, subject_id)
    if subject and subject.user_id == user_id:
        return subject
    return None


@router.get("", response_model=list[ExamOut])
def list_exams(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return db.scalars(select(Exam).where(Exam.user_id == user.id).order_by(Exam.exam_date)).all()


@router.post("", response_model=ExamOut)
def create_exam(payload: ExamCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if not _owned_subject(db, payload.subject_id, user.id):
        raise HTTPException(status_code=404, detail="Subject not found")

    exam = Exam(user_id=user.id, subject_id=payload.subject_id, title=payload.title.strip(), exam_date=payload.exam_date, target_hours=payload.target_hours, priority=payload.priority)
    db.add(exam)
    db.commit()
    db.refresh(exam)
    return exam


@router.put("/{exam_id}", response_model=ExamOut)
def update_exam(exam_id: UUID, payload: ExamUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    exam = db.get(Exam, exam_id)
    if not exam or exam.user_id != user.id:
        raise HTTPException(status_code=404, detail="Exam not found")

    if not _owned_subject(db, payload.subject_id, user.id):
        raise HTTPException(status_code=404, detail="Subject not found")

    exam.subject_id = payload.subject_id
    exam.title = payload.title.strip()
    exam.exam_date = payload.exam_date
    exam.target_hours = payload.target_hours
    exam.priority = payload.priority
    db.commit()
    db.refresh(exam)
    return exam


@router.delete("/{exam_id}")
def delete_exam(exam_id: UUID, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    exam = db.get(Exam, exam_id)
    if not exam or exam.user_id != user.id:
        raise HTTPException(status_code=404, detail="Exam not found")
    db.delete(exam)
    db.commit()
    return {"message": "Deleted"}
