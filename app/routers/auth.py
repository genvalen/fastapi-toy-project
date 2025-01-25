from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, models, utils, database

router = APIRouter(
    prefix = "/login",
    tags = ["Authentication"],
)

@router.post("/")
async def login(credentials: schemas.UserCredentials, db: Session = Depends(database.get_db)):
    # check if email is valid, otherwise raise error
    user = db.query(models.User).filter(models.User.email == credentials.email).first()
    if not user:
        raise HTTPException(
            detail = "Invalid credentials",
            status_code = status.HTTP_404_NOT_FOUND,
        )

    # check if passsword if valid otherwise return error
    if not utils.verify_pwd(credentials.password, user.password):
        raise HTTPException(
            detail = "Invalid credentials",
            status_code = status.HTTP_404_NOT_FOUND
        )

    return {"token": "token placeholder"}
