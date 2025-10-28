from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
import bcrypt
import uuid
from utils.auth import Auth
from database.base import get_db
from ..models.user_model import User
from ..schemas.user_schemas import (UserResponse, UserRegistrationRequest, 
                                    UserLoginRequest, UserUpdateRequest, TokenResponse)

router = APIRouter(prefix="/api/user", tags=["user"])

@router.post('/register', response_model=UserResponse, status_code=201)
async def register_user(user_data: UserRegistrationRequest, db: Session = Depends(get_db)):
    try:
        pw_salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(user_data.password.encode('utf-8'), pw_salt)
        new_user = User(
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            email=user_data.email,
            hashed_password=hashed_password,
            phone_number=user_data.phone_number if user_data.phone_number else ""
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user
    
    except IntegrityError as ie:
        db.rollback()
        raise HTTPException(status_code=400, detail="User with this email or identifier already exists")
    
    except Exception as e:
        db.rollback()
        # Use Logging to log errors for debugging
        raise HTTPException(status_code=500, detail="An unexpected error occured while registering new user")
    
@router.post("/login", response_model=TokenResponse, status_code=200)
async def login_user(user_auth: UserLoginRequest, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.email == user_auth.email).first()
        if not user or not bcrypt.checkpw(user_auth.password.encode('utf-8'), user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        token_data = {
            "id": str(user.id),
            "role": user.role,
            "email": user.email
        }

        access_token = Auth.create_access_token(token_data)

        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            user=user
        )
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")
    
@router.put("/{user_id}", response_model=UserResponse, status_code=200)
async def update_user(user_data: UserUpdateRequest, user_id: uuid.UUID, db: Session= Depends(get_db)):

    try:
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if user_data.first_name:
            user.first_name = user_data.first_name
        if user_data.last_name:
            user.last_name = user_data.last_name
        if user_data.email:
            user.email = user_data.email
        if user_data.phone_number:
            user.phone_number = user_data.phone_number

        db.commit()
        db.refresh(user)
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail="Unable to edit user information.")
    

