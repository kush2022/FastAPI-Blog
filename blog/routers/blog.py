from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from blog import schemas, database, models

from  blog.oauth2 import get_current_user

get_db = database.get_db


router = APIRouter(
    tags=['Blog'],
    prefix='/blog'
)

@router.post('/create')
async def create_blog(request: schemas.Blog, current_user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)

    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog


@router.get('/all')
async def all_blogs(current_user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()


    return blogs


@router.get('/{id}')
async def get_blog(id: int, current_user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The blog with the id {id} is not found")
    
    return blog 


@router.delete('/{id}')
async def delete_blog(id: int, current_user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} is not found")
    blog.delete(synchronize_session=False)
    db.commit()

    return "Delete succussfully"


@router.put('/{id}')
async def update_blog(id: int, request: schemas.Blog,current_user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} is not found")
   
    
    blog.title = request.title
    blog.body = request.body
    db.commit()
    return {"status": "success"}
