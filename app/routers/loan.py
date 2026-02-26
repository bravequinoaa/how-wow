from sqlite3 import IntegrityError
from fastapi import APIRouter, Depends, HTTPException

from app.core.context import get_session
from app.crud.loan import create_loan, read_loan_schedule, read_loans, share_loan, read_loan_summary
from app.schema.loan import LoanCreate, LoanShareCreate
from app.errors import default_400_error



router = APIRouter(
    prefix="/loans",
    tags=["loans"],
    # dependencies=[Depends(log)],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def read_loans_endpoint(db=Depends(get_session)):
    try:
        return read_loans(db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=default_400_error)

@router.post("/")
async def create_loan_endpoint(loan: LoanCreate, db=Depends(get_session)):
    try:
        return create_loan(db, loan)
    except Exception as e:
        raise HTTPException(status_code=400, detail=default_400_error)

@router.get("/{loan_id}/schedule")
async def read_loan_schedule_endpoint(loan_id: int, db=Depends(get_session)):
    try:
        return read_loan_schedule(db, loan_id)
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=400, detail=default_400_error)

@router.post("/{loan_id}/share/")
async def share_loan_endpoint(loan_id: int, loan_share: LoanShareCreate, db=Depends(get_session)):
    try:
        return share_loan(db, loan_id, loan_share)
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail="Loan already shared with this user")
    except Exception as e:
        raise HTTPException(status_code=400, detail=default_400_error)

@router.get("/{loan_id}/summary/{month}")
async def read_loan_summary_endpoint(loan_id: int, month: int, db=Depends(get_session)):
    try:
        return read_loan_summary(db, loan_id, month)
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=400, detail=default_400_error)