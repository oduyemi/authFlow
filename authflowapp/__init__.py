import os
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker
from authflowapp.database import SessionLocal
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from authflowapp.config import SECRET_KEY, DATABASE_URI

runner = FastAPI()

templates = Jinja2Templates(os.path.join(os.path.dirname(__file__), "templates"))
runner.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")


engine = create_engine(DATABASE_URI)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base: DeclarativeMeta = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



from authflowapp import routes

runner.include_router(routes.router, dependencies=[Depends(get_db)])
