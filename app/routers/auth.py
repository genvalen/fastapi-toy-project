from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import schemas, models, utils, database
from ..oauth2 import create_access_token

router = APIRouter(
    prefix = "/login",
    tags = ["Authentication"],
)

@router.post("/")
async def login(credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    # Check if email is valid, otherwise raise error
    # Note: OAuth2PasswordRequestForm has the attribute username instead of email.
    user = db.query(models.User).filter(models.User.email == credentials.username).first()
    if not user:
        raise HTTPException(
            detail = "Invalid credentials",
            status_code = status.HTTP_404_NOT_FOUND,
        )
    # Check if passsword is valid, otherwise return error
    if not utils.verify_pwd(credentials.password, user.password):
        raise HTTPException(
            detail = "Invalid credentials",
            status_code = status.HTTP_404_NOT_FOUND
        )
    access_token = create_access_token(data={"User": user.id})
    return {"Access Token": access_token, "Token Type": "Bearer", }
