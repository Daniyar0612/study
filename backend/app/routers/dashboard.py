from datetime import date, timedelta

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.exam import Exam
from app.models.plan_item import PlanItem, PlanStatus
from app.models.user import User
from app.schemas.dashboard import DashboardStats

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/stats", response_model=DashboardStats)
def get_stats(week_start: date = Query(...), db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    week_end = week_start + timedelta(days=6)

    week_items = db.scalars(
        select(PlanItem).where(PlanItem.user_id == user.id, PlanItem.date >= week_start, PlanItem.date <= week_end)
    ).all()

    total_planned = sum(item.hours for item in week_items)
    completed = sum(item.hours for item in week_items if item.status == PlanStatus.done)
    percent = round((completed / total_planned) * 100, 2) if total_planned else 0.0

    nearest_exam = db.scalar(
        select(Exam)
        .where(Exam.user_id == user.id, Exam.exam_date >= date.today())
        .order_by(Exam.exam_date)
        .limit(1)
    )

    return DashboardStats(
        week_start=week_start,
        total_planned_hours=round(total_planned, 2),
        completed_hours=round(completed, 2),
        completion_percent=percent,
        nearest_exam_title=nearest_exam.title if nearest_exam else None,
        nearest_exam_date=nearest_exam.exam_date if nearest_exam else None,
    )
