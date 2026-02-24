import enum
import uuid
from datetime import date

from sqlalchemy import Date, Enum, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class PlanStatus(str, enum.Enum):
    pending = "pending"
    done = "done"


class PlanItem(Base):
    __tablename__ = "plan_items"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    exam_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("exams.id", ondelete="CASCADE"), nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    hours: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[PlanStatus] = mapped_column(Enum(PlanStatus, name="plan_status"), default=PlanStatus.pending, nullable=False)

    user = relationship("User", back_populates="plan_items")
    exam = relationship("Exam", back_populates="plan_items")
