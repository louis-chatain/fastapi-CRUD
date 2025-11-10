from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    email: str
    password: str

class UserDisplay(BaseModel): # sends back only username and email in the respounse body in the docs
    username: str
    email: str
    class Config():
        orm_mode = True