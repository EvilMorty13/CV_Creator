from pydantic import BaseModel
from typing import List, Optional

class CreateUserRequest(BaseModel):
    email: str
    password: str


class CreateUserResponse(BaseModel):
    email: str
    isAdmin: bool


class CreateProfileRequest(BaseModel):
    name: str
    interestedIn: Optional[List[str]] = []

class CreateProfileResponse(BaseModel):
    user_id: int
    name: str
    interestedIn: List[str]  
        
class Token(BaseModel):
    access_token: str
    token_type: str
