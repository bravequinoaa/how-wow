from sqlite3 import IntegrityError
from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import List, Union

from app.crud.loan_calculations import calculate_monthly_interest_rate, calculate_loan_monthly_payment_zero_interest, calculate_loan_amortization, generate_loan_schedule
from app.models.loan import Loan
from app.models.loan_share import LoanShare
from app.models.user import User
from app.schema.loan import LoanCreate, LoanShareCreate

def create_loan(db: Session, loan: LoanCreate) -> Loan:
# def create_user(db: Session, user: UserCreate) -> User:
    print(f'Creating loan for user {loan.username} with amount {loan.amount}, annual interest rate {loan.annual_interest_rate}, term {loan.loan_term_in_months} months')
    db_loan = Loan(
        owner_username=loan.username,
        amount=loan.amount,
        annual_interest_rate=loan.annual_interest_rate,
        loan_term_in_months=loan.loan_term_in_months
    )
    db.add(db_loan)
    db.commit()
    db.refresh(db_loan)
    return db_loan

def read_loans(db: Session) -> List[Loan]:
    return db.query(Loan).all()

def read_loan_schedule(db: Session, loan_id: int) -> List[dict]:
    print(f'grabbing loan schedule for loan id {loan_id}')
    loan =  validate_loan_exists(db, loan_id)
    if loan:
        print(f'Loan id {loan_id} exists, proceeding to calculate schedule')
    
    monthly_interest_rate = calculate_monthly_interest_rate(float(loan.annual_interest_rate))
    number_of_payments = int(loan.loan_term_in_months)
    if monthly_interest_rate == 0:
        # If interest rate is 0, simply divide principal by number of payments
        monthly_payment = calculate_loan_monthly_payment_zero_interest(loan.amount, number_of_payments)
    else:
        # Calculate monthly payment using the amortization formula
        monthly_payment = calculate_loan_amortization(loan.amount, monthly_interest_rate, number_of_payments)
    print(f'Calculated monthly payment: {monthly_payment}')
    
    remaining_balance = float(loan.amount)
    print(f'Starting amortization schedule calculation with balance: {remaining_balance}')

    schedule = generate_loan_schedule(remaining_balance, monthly_interest_rate, monthly_payment, number_of_payments)
    
    return schedule

def share_loan(db: Session, loan_id: int, loan_share: LoanShareCreate) -> LoanShare:
    print(f'Sharing loan id {loan_id} with user {loan_share.shared_with_username}')
    if validate_loan_exists(db, loan_id):
        print(f'Loan id {loan_id} exists -- checking user {loan_share.shared_with_username}')

    if validate_user_exists(db, loan_share.shared_with_username):
        print(f'User {loan_share.shared_with_username} exists -- proceeding to share loan')

    db_loan_share = LoanShare(
        loan_id=loan_id,
        shared_with_username=loan_share.shared_with_username
    )
    db.add(db_loan_share)
    db.commit()
    db.refresh(db_loan_share)
    return db_loan_share

def read_loan_summary(db: Session, loan_id: int, month: int) -> Union[dict, HTTPException]:
    print(f'Grabbing loan summary for loan id {loan_id} at month {month}')

    # get whole schedule and return month requested
    schedule = read_loan_schedule(db, loan_id)
    if month < 1 or month > len(schedule):
        raise HTTPException(status_code=400, detail="Invalid month number")
    
    return schedule[month - 1]  # month is 1-indexed


# UTIL FUNCTIONS
def validate_user_exists(db: Session, username: str):
    user = grab_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def grab_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def validate_loan_exists(db: Session, loan_id: int):
    loan = grab_loan_by_id(db, loan_id)
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    return loan
        
def grab_loan_by_id(db: Session, loan_id: int) -> Loan:
    return db.query(Loan).filter(Loan.loan_id == loan_id).first()