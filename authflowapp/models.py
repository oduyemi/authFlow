from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from authflowapp.database import Base

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class User(Base):
    __tablename__ = "user"
    user_id = Column(Integer, autoincrement=True, primary_key=True)
    user_fname = Column(String(100))
    user_lname = Column(String(100))
    user_email = Column(String(100), unique=True)
    user_password = Column(String(200))
    user_regdate = Column(DateTime(), default=datetime.utcnow)
    confirmation_token = Column(String(100), nullable=True)


