from webbrowser import get

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.orm.strategies import query

import models
import schemas
from auth import create_token, verify_token
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine) #table will create

app = FastAPI()
# DB Dependency
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Login API
@app.post("/login")
def login():
    return{
        "access_token": create_token({"user": "admin"}),
        "token_type": "bearer"
    }



# Home Route
@app.get("/")
def home():
    return{
        "message":"Blog API Started!"
    }

# Create Blog - Protected
@app.post("/blogs", response_model=schemas.BlogResponse)
def create_blog(blog: schemas.BlogCreate, db:Session=Depends(get_db), user = Depends(verify_token)):
    new_blog=models.Blog(
        title=blog.title,
        content=blog.content
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog

@app.get("/blogs", response_model=list[schemas.BlogResponse])
def get_blogs(db: Session= Depends(get_db)):
    return db.query(models.Blog).all()

# Read One Blog
@app.get("/blogs/{id}", response_model=schemas.BlogResponse)
def get_blog(id:int, db:Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog

# Update Blog API - Protected
@app.put("/blogs/{id}", response_model=schemas.BlogResponse)
def update_blog(id:int, blog:schemas.BlogCreate, db:Session = Depends(get_db), user = Depends(verify_token)):
    existing_blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not existing_blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    existing_blog.title = blog.title
    existing_blog.content = blog.content

    db.commit()
    db.refresh(existing_blog)

    return existing_blog

# Delete Blog API - protected
@app.delete("/blogs/{id}")
def delete_blog(id:int, db:Session=Depends(get_db), user = Depends(verify_token)):
    blog_to_delete = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog_to_delete:
        raise HTTPException(status_code=404, detail="Blog not found")

    db.delete(blog_to_delete)
    db.commit()

    return{
        "message": f"Blog with ID: {blog_to_delete.id} Deleted"
    }
