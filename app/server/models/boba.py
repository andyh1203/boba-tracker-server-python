from typing import Option
from datetime import datetime

from pydantic import BaseModel


class Boba(BaseModel):
    drink_name: str
    sugarLevel: str
    iceLevel: str
    createdAt: datetime
    updatedAt: datetime