from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str
    email: str

    class Config:
        from_attributes = True