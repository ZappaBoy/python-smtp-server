from typing import Optional, Any

from pydantic import BaseModel


class Attachment(BaseModel):
    file: Optional[Any]
    filename: Optional[str]
