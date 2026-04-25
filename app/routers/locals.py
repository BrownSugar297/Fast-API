from fastapi import APIRouter,HTTPException,status,Response,Depends
from httpx import post
from .. import models
from .. database import get_db
from sqlalchemy.orm import Session
from .. schemas import  Student_Create,Student_Response
from .. import oauth2
from .. import schemas


router=APIRouter(
    prefix="/locals",
    tags=["Locals"]
    
)


#alchemy
@router.get("/",response_model=list[schemas.Student_Response])
def get_locals(db: Session = Depends(get_db), current_user: models.Stoners = Depends(oauth2.get_current_user)):
    locals = db.query(models.Student).all()
    return locals



#alchemy
@router.get("/{id}",response_model=Student_Response)
def get_local(id: int, db: Session = Depends(get_db), current_user: models.Stoners = Depends(oauth2.get_current_user)):
    local = db.query(models.Student).filter(models.Student.id == id).first()
    if not local:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Local with id {id} not found")
    return local



#alchemy
@router.post("/", response_model=Student_Response)
def create_local(local: Student_Create, db: Session = Depends(get_db),  current_user: models.Stoners = Depends(oauth2.get_current_user)):
        print(current_user.id)
        print(current_user.name)
        new_local = models.Student(**local.model_dump())
        db.add(new_local)
        db.commit()
        db.refresh(new_local)
        return new_local




#alchemy
@router.put("/{id}", response_model=Student_Response)
def update_local(id: int, student_data: Student_Create, db: Session = Depends(get_db), current_user: models.Stoners = Depends(oauth2.get_current_user)):
    local = db.query(models.Student).filter(models.Student.id == id)
    existing_student = local.first()

    if not existing_student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Local with id {id} not found"
        )

    local.update(student_data.model_dump(), synchronize_session=False)
    db.commit()
    db.refresh(existing_student)

    return {"details": existing_student}


#alchemy
@router.delete("/{id}" , status_code=status.HTTP_204_NO_CONTENT)
def delete_local(id: int, db: Session = Depends(get_db), current_user: models.Stoners = Depends(oauth2.get_current_user)):
    local = db.query(models.Student).filter(models.Student.id == id)
    existing_local = local.first()
    if not existing_local:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Local with id {id} not exist")
    local.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

