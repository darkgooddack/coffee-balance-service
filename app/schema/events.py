from pydantic import BaseModel


class AuthRequest(BaseModel):
    request_id: str
    token: str


class AuthResponse(BaseModel):
    request_id: str
    user_id: str | None = None
    error: str | None = None
