from fastapi import APIRouter,status,Depends
from httpx import post
from .. import models,utils
from .. database import get_db
from sqlalchemy.orm import Session
from .. schemas import Stoner_Create, Stoner_Response


router=APIRouter(
    prefix="/stoners",
    tags=["Stoners"]
    
)




@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Stoner_Response)
def create_stoner(stoner: Stoner_Create, db: Session = Depends(get_db)):
    
    stoner_data = stoner.model_dump()  
    stoner_data["password"] = utils.hash_password(stoner_data["password"])
    new_stoner = models.Stoners(**stoner_data)
    
    db.add(new_stoner)
    db.commit()
    db.refresh(new_stoner)
    
    return new_stoner