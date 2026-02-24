from pydantic import BaseModel


class PlanStatusUpdate(BaseModel):
    status: str
