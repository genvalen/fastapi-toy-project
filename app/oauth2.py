import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta, timezone
from fastapi import status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Dict, Union

from . import schemas

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")  # arg should be endpoint for logging in

SECRET_KEY = "5a0e659da9290463df07dd6485b82ac12e4cb1319e04ca3cb69b00d35c7ae18e"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: Dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verfiy_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("User")
        if not user_id:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    token_data = schemas.TokenData(id=user_id)  # token data currenly only contains ID info
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Verify the token of the current user. If verfied, return user ID.
    """
    credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "Could not verify credentials",
        headers = {"WWW-Authenticate": "Bearer"},
    )
    return verfiy_access_token(token, credentials_exception)

