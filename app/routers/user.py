from fastapi import APIRouter, Depends, HTTPException

from app.core.context import get_session
from app.crud.user import read_user, create_user, read_user_loans
from app.schema.user import UserCreate
from app.errors import default_400_error


router = APIRouter(
    prefix="/users",
    tags=["users"],
    # dependencies=[Depends(log)],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def read_users_endpoint(db=Depends(get_session)):
    try:
        return read_user(db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=default_400_error)

@router.post("/")
async def create_user_endpoint(user: UserCreate, db=Depends(get_session)):
    try:
        return create_user(db, user)
    except Exception as e:  
        raise HTTPException(status_code=400, detail=default_400_error)

@router.get("/{username}/loans")
async def read_user_loans_endpoint(username: str, db=Depends(get_session)):
    try:
        return read_user_loans(db, username)
    except Exception as e:
        raise HTTPException(status_code=400, detail=default_400_error)