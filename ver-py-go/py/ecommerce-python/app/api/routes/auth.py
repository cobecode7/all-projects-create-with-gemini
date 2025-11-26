
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import create_access_token
from app.models.user import User
from app.schemas.user import UserResponse, Token, LoginRequest, UserCreate
from app.services.auth import register_user, authenticate_user
from app.api.dependencies import get_current_active_user

router = APIRouter()

@router.post("/register", response_model=Token)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user
    """
    return register_user(user_data, db)

@router.post("/login", response_model=Token)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """
    Authenticate user and return access token
    """
    return authenticate_user(login_data, db)

@router.post("/refresh", response_model=Token)
def refresh_token(current_user: User = Depends(get_current_active_user)):
    """
    Refresh access token
    """
    access_token = create_access_token(data={"sub": str(current_user.id)})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse.from_orm(current_user)
    }
