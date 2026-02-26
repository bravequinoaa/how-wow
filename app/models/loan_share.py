from sqlalchemy import Column, String, Integer, Numeric, ForeignKey
from sqlalchemy.orm import  relationship

from app.models.base import Base

class LoanShare(Base):
    __tablename__ = 'LoanShare'

    loan_id = Column(Integer, ForeignKey('loan.loan_id', ondelete="CASCADE"), primary_key=True, autoincrement=True)
    shared_with_username = Column(String(256), ForeignKey('User.username', ondelete="CASCADE"), primary_key=True, nullable=False)

    # Relationships
    loan = relationship("Loan")
    user = relationship('User')

    def __repr__(self):
        return f'Loan_Share(loan_id={self.loan_Id}, shared_with_username={self.shared_with_username}'
    