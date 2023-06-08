from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from blog import schemas, database, models, jwt_token
from blog.hashing import Hash

get_db = database.get_db

router = APIRouter(
    tags=['User'],
    prefix='/user'
)


@router.post('/create', status_code=status.HTTP_200_OK)
async def create_user(request: schemas.User, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.email).first()

    if user is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'The user with the {request.email} exists')
    

    new_user = models.User(name=request.name, email=request.email, password=Hash.bcrypt(request.password))

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post('/login')
async def login_user(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    
    if not Hash.verify(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, details='Incorrect password')
    
    access_token = jwt_token.create_access_token(data={"sub": user.email})

    return {"access_token": access_token, "token_type": "bearer"}