from pydantic import BaseModel, EmailStr
from typing import Optional

class ProfileBase(BaseModel):
    bio: Optional[str] = "Hello world!"

class Profile(ProfileBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True