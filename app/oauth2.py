import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta, timezone
from typing import Union

SECRET_KEY = "5a0e659da9290463df07dd6485b82ac12e4cb1319e04ca3cb69b00d35c7ae18e"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
