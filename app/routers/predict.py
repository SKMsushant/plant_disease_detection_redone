from pathlib import Path
import uuid 
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter,UploadFile,File
from fastapi.params import Body
from pydantic import BaseModel,EmailStr
from typing import Optional,List

from datetime import datetime
import time
from sqlalchemy.orm import Session
from ..database import get_db
from ..db_models.user import Users
from ..services import auth_service



from ..db_models import prediction
from ..services.model_service import predictor
from ..config import settings

router=APIRouter(
    prefix="/predict",
    tags=['inference']
)

ALLOWED_EXTENSIONS = {"image/jpeg", "image/png", "image/webp"}

@router.post("",response_model=prediction.PredictionResponse)
async def predict_plant_disease(
    file:UploadFile=File(...),
    db:Session=Depends(get_db),
    current_user:Users=Depends(auth_service.get_current_user_final),):
    if file.content_type not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type: {file.content_type}. Only JPEG, PNG, and WebP are allowed."
        )
    try:
        user_upload_dir=Path(settings.UPLOAD_DIR)/f"user_{current_user.id}"
        user_upload_dir.mkdir(parents=True,exist_ok=True)

        unique_filename=f"{uuid.uuid4().hex[:8]}_{file.filename}"
        saved_filepath=user_upload_dir/unique_filename

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Unable to save the file")

    try:
        image_bytes=await file.read()
        with open(saved_filepath,'wb') as f:
            f.write(image_bytes)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error reading image: {str(e)}"
        )

    try:
        result = predictor.predict(image_bytes,filename=unique_filename)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Inference error: {str(e)}"
        )
    new_prediction=prediction.Predictions(
        user_id=current_user.id,
        original_filename=file.filename,
        stored_path=str(saved_filepath),
        predicted_class=result['condition'],
        confidence=result['confidence']
    )

    db.add(new_prediction)
    db.commit()
    db.refresh(new_prediction)

    return result

@router.get('/history')
def get_user_history(db:Session=Depends(get_db),current_user:Users=Depends(auth_service.get_current_user_final)):
    history=db.query(prediction.Predictions).filter(prediction.Predictions.user_id==current_user.id).order_by(prediction.Predictions.created_at.desc()).all()

    return history