"""Model containing Data Transfer Objects across the different layers"""
from pydantic import BaseModel


class RandomNameCreationRequestDTO(BaseModel):
    length: int


class MessageDTO(BaseModel):
    message: str


class NameCreationRequestDTO(BaseModel):
    title: str


class NameRecordDTO(BaseModel):
    id: int
    title: str

    class Config:
        orm_mode = True
