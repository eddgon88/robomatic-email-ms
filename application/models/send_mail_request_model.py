from pydantic import BaseModel
from typing import Optional
from pydantic import EmailStr, BaseModel
from typing import List

class SendMailRequestModel(BaseModel):
    email: List[EmailStr]
    subject: str
    body: Optional[str] = None
    body_dict: Optional[dict] = None
    template_id: Optional[str] = None
    files: Optional[List[str]] = None