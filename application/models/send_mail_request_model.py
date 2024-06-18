from pydantic import BaseModel, EmailStr
from typing import Optional, List

class SendMailRequestModel(BaseModel):
    email: List[EmailStr]
    subject: str
    body: Optional[str] = None
    body_dict: Optional[dict] = None
    template_id: Optional[str] = None
    files: Optional[List[str]] = None