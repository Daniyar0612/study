from datetime import date

from pydantic import BaseModel


class DashboardStats(BaseModel):
    week_start: date
    total_planned_hours: float
    completed_hours: float
    completion_percent: float
    nearest_exam_title: str | None
    nearest_exam_date: date | None
