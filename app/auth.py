from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from .database import get_db
from .models import Appointment
from .schemas import AuthRequest, Token

SECRET_KEY = "exam-secret-key-change-me"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def authenticate_user(auth_data: AuthRequest, db: Session) -> str:
    """
    Verify that the phone number and SMS code pair exists in the DB.
    Returns phone number if authentication succeeds, otherwise raises HTTPException.
    """
    appointment = (
        db.query(Appointment)
        .filter(
            Appointment.phone_number == auth_data.phone_number,
            Appointment.sms_code == auth_data.sms_code,
        )
        .first()
    )
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверная пара номер телефона - код из СМС",
        )
    return appointment.phone_number


def get_current_phone(token: str = Depends(oauth2_scheme)) -> str:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось проверить токен доступа",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        phone: str | None = payload.get("sub")
        if phone is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return phone


def login(auth_data: AuthRequest, db: Session) -> Token:
    phone = authenticate_user(auth_data, db)
    access_token = create_access_token(data={"sub": phone})
    return Token(access_token=access_token)

