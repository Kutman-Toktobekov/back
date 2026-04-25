from pydantic import BaseModel


class UserCreate(BaseModel):
    email: str
    password: str


class ReportCreate(BaseModel):
    title: str
    description: str
    lat: float
    lng: float


class StatusUpdate(BaseModel):
    status: str