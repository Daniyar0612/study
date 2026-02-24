from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.subject import Subject
from app.models.user import User
from app.schemas.common import SubjectOut
from app.schemas.subject import SubjectCreate, SubjectUpdate

router = APIRouter(prefix="/subjects", tags=["subjects"])


@router.get("", response_model=list[SubjectOut])
def list_subjects(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return db.scalars(select(Subject).where(Subject.user_id == user.id).order_by(Subject.name)).all()


@router.post("", response_model=SubjectOut)
def create_subject(payload: SubjectCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    subject = Subject(user_id=user.id, name=payload.name.strip())
    db.add(subject)
    db.commit()
    db.refresh(subject)
    return subject


@router.put("/{subject_id}", response_model=SubjectOut)
def update_subject(subject_id: UUID, payload: SubjectUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    subject = db.get(Subject, subject_id)
    if not subject or subject.user_id != user.id:
        raise HTTPException(status_code=404, detail="Subject not found")
    subject.name = payload.name.strip()
    db.commit()
    db.refresh(subject)
    return subject


@router.delete("/{subject_id}")
def delete_subject(subject_id: UUID, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    subject = db.get(Subject, subject_id)
    if not subject or subject.user_id != user.id:
        raise HTTPException(status_code=404, detail="Subject not found")
    db.delete(subject)
    db.commit()
    return {"message": "Deleted"}
