from typing import Optional

from pydantic import BaseModel, validator


class Receiver(BaseModel):
    name: Optional[str]
    last_name: Optional[str]
    complete_name: Optional[str]
    email: Optional[str]

    @validator('complete_name', always=True)
    def set_complete_name(cls, v, values, **kwargs):
        return v or f'{values["name"]} {values["last_name"]}' if values.get('name') and values.get(
            'last_name') else None
