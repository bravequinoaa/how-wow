
from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    firstname: str
    lastname: str
    phone: str
    address: str
    email: str