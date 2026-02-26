from sqlalchemy.orm import Session
from typing import List

from app.models.user import User
from app.models.loan import Loan
from app.schema.user import UserCreate

def create_user(db: Session, user: UserCreate) -> User:
# def create_user(db: Session, user: UserCreate) -> User:
    db_user = User(
        username=user.username,
        firstname=user.firstname,
        lastname=user.lastname,
        phone=user.phone,
        address=user.address,
        email=user.email
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def read_user(db: Session) -> List[User]:
    return db.query(User).all()

def read_user_loans(db: Session, username: str):
    return db.query(Loan).where(Loan.owner_username == username).all()