from fastapi import APIRouter, HTTPException, status, Depends,responses
from sqlalchemy.orm import Session
from .. import models, utils,database,schemas,oauth2
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta


router = APIRouter(
    tags=["Authentication"]
)

@router.post("/login")
def login(credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    stoner = db.query(models.Stoners).filter(models.Stoners.email == credentials.username).first()
    
    if not stoner or not utils.verify_password(credentials.password, stoner.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    
    access_token = oauth2.create_access_token(
        data={"user_id": stoner.id},
        expires_delta = timedelta(minutes=oauth2.ACCESS_TOKEN_EXPIRE_MINUTES)
    )


    return {"access_token": access_token, "token_type": "bearer"} 