from datetime import date, timedelta
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.exam import Exam
from app.models.plan_item import PlanItem, PlanStatus
from app.models.user import User
from app.schemas.common import PlanItemOut
from app.schemas.plan import PlanStatusUpdate
from app.services.plan_generator import generate_exam_allocations

router = APIRouter(prefix="/plan", tags=["plan"])


@router.post("/generate")
def generate_plan(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    today = date.today()
    db.execute(delete(PlanItem).where(PlanItem.user_id == user.id, PlanItem.date >= today))

    exams = db.scalars(select(Exam).where(Exam.user_id == user.id, Exam.exam_date >= today)).all()
    allocations = generate_exam_allocations(exams, today)

    for (exam_id, dt), hours in allocations.items():
        if hours <= 0:
            continue
        db.add(PlanItem(user_id=user.id, exam_id=UUID(exam_id), date=dt, hours=hours, status=PlanStatus.pending))

    db.commit()
    return {"created_items": len(allocations)}


@router.get("", response_model=list[PlanItemOut])
def get_plan_for_day(date: date = Query(...), db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return db.scalars(select(PlanItem).where(PlanItem.user_id == user.id, PlanItem.date == date).order_by(PlanItem.hours.desc())).all()


@router.get("/week", response_model=list[PlanItemOut])
def get_plan_week(start: date = Query(...), db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    end = start + timedelta(days=6)
    return db.scalars(select(PlanItem).where(PlanItem.user_id == user.id, PlanItem.date >= start, PlanItem.date <= end).order_by(PlanItem.date)).all()


@router.patch("/{plan_item_id}", response_model=PlanItemOut)
def update_plan_status(plan_item_id: UUID, payload: PlanStatusUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    plan_item = db.get(PlanItem, plan_item_id)
    if not plan_item or plan_item.user_id != user.id:
        raise HTTPException(status_code=404, detail="Plan item not found")
    if payload.status not in ("pending", "done"):
        raise HTTPException(status_code=400, detail="Invalid status")

    plan_item.status = PlanStatus(payload.status)
    db.commit()
    db.refresh(plan_item)
    return plan_item
