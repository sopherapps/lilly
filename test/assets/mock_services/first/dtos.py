"""Model containing Data Transfer Objects across the different layers"""
from pydantic import BaseModel


class MessageDTO(BaseModel):
    message: str
