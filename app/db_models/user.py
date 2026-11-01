from ..database import Base
from sqlalchemy import Column,Integer,String,Boolean,Float,Identity,ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP,DateTime
from sqlalchemy import text
from sqlalchemy.orm import relationship


class Users(Base):
    __tablename__='users'
    id=Column(Integer,Identity(start=1,increment=1),primary_key=True,nullable=False)
    name=Column(String(100),nullable=False)
    email=Column(String(255),nullable=False,unique=True)
    phonenumber=Column(String,nullable=False,unique=True)
    hashed_password=Column(String,nullable=False,)
    totp_secret=Column(String,nullable=False)
    is_2fa_enabled=Column(Boolean,default=False,)
    created_at=Column(DateTime(timezone=True),server_default=text('now()'),nullable=False)
    predictions=relationship('Predictions',back_populates='users')