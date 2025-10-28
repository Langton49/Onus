from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from config import server_settings
from schemas.user_schemas import TokenData
from models.user_model import User
from sqlalchemy.orm import Session
from database.base import get_db
from schemas.user_schemas import UserResponse

secret_key = server_settings.JWT_SECRET_KEY
algorithm = server_settings.ALGORITHM
token_expiry = server_settings.ACCESS_TOKEN_EXPIRY

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/login")  # token endpoint

class Auth:
    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        now = datetime.now(timezone.utc)
        if expires_delta:
            expire = now + expires_delta
        else:
            expire = now + timedelta(minutes=token_expiry)
        to_encode.update({"exp": expire, "iat": now})
        encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
        return encoded_jwt

    @staticmethod
    def verify_token(token: str) -> TokenData:
        try:
            payload = jwt.decode(token, secret_key, algorithms=[algorithm])
            id = payload.get("id")
            role = payload.get("role")
            email = payload.get("email")
            if id is None or role is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
            return TokenData(id=id, role=role, email=email)
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

    @staticmethod
    def get_current_token_data(token: str = Depends(oauth2_scheme)) -> TokenData:
        return Auth.verify_token(token)

    @staticmethod
    def get_current_user(token_data: TokenData = Depends(get_current_token_data), db: Session = Depends(get_db)) -> UserResponse:
        user = db.query(User).filter(User.id == token_data.id).first()
        if not user or not user.is_active:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Inactive user")
        
        return UserResponse.model_validate(user)

    @staticmethod
    def require_role(required_role: str):
        def _require_role(token_data: TokenData = Depends(Auth.get_current_token_data)):
            if token_data.role != required_role:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
            return token_data
        return _require_role

    @staticmethod
    def require_any_role(*allowed_roles):
        def _require_any(token_data: TokenData = Depends(Auth.get_current_token_data)):
            if token_data.role not in allowed_roles:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
            return token_data
        return _require_any