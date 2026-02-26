
from pydantic import BaseModel

class LoanCreate(BaseModel):
    username: str
    amount: float
    annual_interest_rate: float
    loan_term_in_months: int

class LoanShareCreate(BaseModel):
    shared_with_username: str