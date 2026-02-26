from sqlalchemy import Column, String, Integer, Numeric, ForeignKey
from sqlalchemy.orm import  relationship

from app.models.base import Base

class Loan(Base):
    __tablename__ = 'loan'

    loan_id = Column(Integer, primary_key=True, autoincrement=True)
    owner_username = Column(String(255), ForeignKey('User.username'), nullable=False)
    amount = Column(Numeric, nullable=False)
    annual_interest_rate = Column(Numeric, nullable=False)
    loan_term_in_months = Column(Numeric)

    # Relationship to User
    user = relationship('User', back_populates='loans')
    loanshares = relationship('LoanShare', back_populates='loan')

    def __repr__(self):
        return f'Loan(loan_id={self.loan_id}, username={self.username}, amount={self.amount},'\
            + f' annual_interest_rate={self.annual_interest_rate}, loan_term_in_months={self.loan_term_in_months})'
    
    def to_response(self):
        response_dict = {}
        response_dict['month'] = None
        response_dict['remaining_balance'] = self.amount
        response_dict['monthly_payment'] = None

        return response_dict