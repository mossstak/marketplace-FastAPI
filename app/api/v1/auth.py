from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ...database import get_db
from ...crud import accounts as crud_accounts
from ...utils.security import create_access_token

router = APIRouter()

@router.post("/register")
def register(username: str, email: str, password: str, db: Session = Depends(get_db)):
    if crud_accounts.get_user_by_username(db, username):
        raise HTTPException(status_code=400, detail="Username already registered")
    if crud_accounts.get_user_by_email(db, email):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user = crud_accounts.create_user(db, username, email, password)
    crud_accounts.create_profile(db, user.id)
    
    return {"message": "User registered successfully", "user_id": user.id}

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud_accounts.get_user_by_username(db, form_data.username)
    
    if not user or not user.verify_password(form_data.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    access_token = create_access_token(data={"sub": user.username, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}