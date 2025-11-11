from pydantic import BaseModel

class UserBase(BaseModel):  # data that we will receive from the user
    username: str
    email: str
    password: str

class UserDisplay(BaseModel): # data that we will receive from the user
    username: str               # sends back only username and email in
    email: str                  # the response body in the docs
    id: int
    class Config():
        orm_mode = True