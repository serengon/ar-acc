from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    email: str = Field(max_length=254)
    password: str = Field(min_length=8, max_length=128)
    invite_code: str = ""


class UserResponse(BaseModel):
    id: str
    email: str
    created_at: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
