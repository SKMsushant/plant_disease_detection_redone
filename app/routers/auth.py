from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from datetime import datetime,timezone,timedelta

from ..schemas import user
from ..database import get_db
from ..db_models.user import Users
from ..services import auth_service

router=APIRouter(
    prefix=('/auth'),
    tags=['Authentication']
)

@router.post('/register',status_code=status.HTTP_201_CREATED,response_model=user.UserRegisterResponse)
def register_user(user_data:user.UserRegister,db:Session=Depends(get_db)):
    user_data_dict=user_data.model_dump(exclude_unset=True)
    existing_emails=[]
    existing_phonenumbers=[]
    for e in db.query(Users.email).all():
        existing_emails.append(e[0])

    for p in db.query(Users.phonenumber).all():
        existing_phonenumbers.append(p[0])

    if (user_data.email in existing_emails) or (user_data.phonenumber in existing_phonenumbers):
        existing_user=db.query(Users).filter((Users.email==user_data.email) | (Users.phonenumber==user_data.phonenumber)).first()

        if (existing_user.is_2fa_enabled) or (existing_user.is_2fa_enabled):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="User is already registerd. Please Login.....")
        
        time_elapsed=datetime.now(timezone.utc)-existing_user.created_at
        if time_elapsed>timedelta(minutes=30):
            db.delete(existing_user)
            db.commit()
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Registration pending. Please log in with your password to complete 2FA."
                )

    hashed_password=auth_service.hash_password(user_data_dict['password'])
    user_data_dict['hashed_password']=hashed_password
    del user_data_dict['password']

    totp_secret=auth_service.generate_totp_secret()
    user_data_dict['totp_secret']=totp_secret
    
    user_data_dict['is_2fa_enabled']=False
    new_user=Users(**user_data_dict)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    qr_code=auth_service.generate_qrcode_email(email=user_data.email,secret=totp_secret) 

    user_return={
        "email":user_data.email,
        'secret':totp_secret,
        "qr_code_base64":qr_code
    }

    return user_return


@router.post("/verify_2fa_setup")
def verify_2fa_code(user_payload:user.Verify2FASetup,db:Session=Depends(get_db)):
    if user_payload.email:
        user_info=db.query(Users).filter(Users.email==user_payload.email).first()
        if not user_info:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='User not found')

        is_valid=auth_service.verify_totp_code(user_info.totp_secret,code=user_payload.otp)
        if not is_valid:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Invalid 2FA code")
    if user_payload.phonenumber:
        user_info=db.query(Users).filter(Users.phonenumber==user_payload.phonenumber).first()
        if not user_info:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='User not found')

        is_valid=auth_service.verify_totp_code(user_info.totp_secret,code=user_payload.otp)
        if not is_valid:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Invalid 2FA code")
    user_info.is_2fa_enabled=True
    db.commit()
    return {'message':'2FA successfully Activated ,you can now login'}


@router.post("/login",response_model=user.LoginResponse)
def user_login(user_cred:user.UserLogin,db:Session=Depends(get_db)):
    if user_cred.email:
        user=db.query(Users).filter(Users.email==user_cred.email).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Invalid Credentials')
        if not auth_service.verify_password(user_cred.password,user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Invalid Credentials')
        if not user.is_2fa_enabled:
            qr_code=auth_service.generate_qrcode_email(email=user.email,secret=user.totp_secret)
            return {
            "status": "2FA_SETUP_PENDING",
            "message": "You have not completed 2FA setup yet. Scan this QR code and verify.",
            "qr_code": qr_code
            }
        temp_token=auth_service.create_temp_access_token(email=user.email)

        return {
            "status":'2FA REQUIRED',
            "temp_token":temp_token
        }
    if user_cred.phonenumber:
        user=db.query(Users).filter(Users.phonenumber==user_cred.phonenumber).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Invalid Credentials')
        if not auth_service.verify_password(user_cred.password,user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Invalid Credentials')
        if not user.is_2fa_enabled:
            qr_code=auth_service.generate_qrcode_phone(phone=user.phonenumber,secret=user.totp_secret)
            return {
            "status": "2FA_SETUP_PENDING",
            "message": "You have not completed 2FA setup yet. Scan this QR code and verify.",
            "qr_code": qr_code
            }
        temp_token=auth_service.create_temp_access_token(email=user.email)

        return {
            "status":'2FA REQUIRED',
            "temp_token":temp_token
        }



@router.post('/login-2fa',response_model=user.LoginResponse)
def user_login_2fa(user_payload:user.Verify2FALogin,db:Session=Depends(get_db)):
    temp_token_payload=auth_service.verify_temp_token(user_payload.temp_token)
    if not temp_token_payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Please Do Login First")
    
    user_info=db.query(Users).filter(Users.email==temp_token_payload.email).first()
    if not user_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    is_valid=auth_service.verify_totp_code(secret=user_info.totp_secret,code=user_payload.code)
    if not is_valid:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid 2FA Code")

    access_token=auth_service.create_access_token(data={'sub':user_info.email})

    return {
        "status":'SUCCESS',
        "access_token":access_token,
        "token_type":'bearer'
    }