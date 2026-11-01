from pydantic import BaseModel
from typing import List
from ..database import Base
from sqlalchemy import Column,Integer,String,Boolean,Float,Identity,ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP,DateTime
from sqlalchemy import text
from sqlalchemy.orm import relationship
from ..db_models.user import Users

class RemedyInfo(BaseModel):
    disease:str
    actions:List[str]

class PredictionResponse(BaseModel):
    filename:str
    plant:str
    condition:str
    is_healthy:bool
    confidence:float
    remedy:RemedyInfo


class Predictions(Base):
    __tablename__='predictions'
    id=Column(Integer,Identity(start=1,increment=1),primary_key=True)  
    user_id=Column(Integer, ForeignKey("users.id",ondelete="CASCADE"),nullable=False) 
    original_filename=Column(String, nullable=False)  
    stored_path=Column(String, nullable=False) 
    predicted_class=Column(String, nullable=False)
    confidence=Column(Float, nullable=False)    
    created_at=Column(DateTime(timezone=True), default=text('now()'),nullable=False)
    users=relationship("Users", back_populates="predictions")