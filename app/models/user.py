from sqlalchemy import Column, String, Integer, Numeric, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

from app.models.base import Base

class User(Base):
    __tablename__ = 'User'

    username = Column(String(255), primary_key=True)
    firstname = Column(String(100), nullable=False)
    lastname = Column(String(100), nullable=False)
    phone = Column(String(10), nullable=False)
    address = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)

    # Relationship to Loan
    loans = relationship('Loan', back_populates='user', cascade='all, delete-orphan')

    def __repr__(self):
        return f'User(username={self.username}, firstname={self.firstname})'

