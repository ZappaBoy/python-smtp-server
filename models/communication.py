from typing import Optional, List

from pydantic import BaseModel

from models.receiver import Receiver


class Communication(BaseModel):
    sender: str
    title: str
    description: str
    receivers: Optional[List[Receiver]] = []
