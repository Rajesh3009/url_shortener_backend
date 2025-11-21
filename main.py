from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import uvicorn
import string
import random

from app import models, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

def generate_short_code(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/shorten")
def shorten(url: str, db: Session = Depends(get_db)):
    # Check if URL already exists (optional, but good for optimization)
    # For now, we'll just create a new one every time as per "basic" requirement
    short_code = generate_short_code()
    db_url = models.URL(original_url=url, short_code=short_code)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return {"short_code": short_code, "original_url": url}

@app.get("/l/{short_code}")
def redirect_url(short_code: str, db: Session = Depends(get_db)):
    db_url = db.query(models.URL).filter(models.URL.short_code == short_code).first()
    if db_url is None:
        raise HTTPException(status_code=404, detail="URL not found")
    
    db_url.clicks += 1
    db.commit()
    db.refresh(db_url)
    
    return {"original_url": db_url.original_url, "clicks": db_url.clicks,"created_at": db_url.created_at}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
