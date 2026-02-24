from pydantic import BaseModel, Field


class SubjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)


class SubjectUpdate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
