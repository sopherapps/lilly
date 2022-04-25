"""Model containing Data Transfer Objects across the different layers"""
from pydantic import BaseModel


class NameCreationRequestDTO(BaseModel):
    length: int


class MessageDTO(BaseModel):
    message: str


class NameRecordDTO(BaseModel):
    id: str
    title: str

    class Config:
        orm_mode = True
