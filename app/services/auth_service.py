from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import pyotp
import qrcode
import base64
import io
from jose import JWTError,jwt
from datetime import datetime,timezone,timedelta
from fastapi.security import OAuth2PasswordBearer,HTTPBearer,HTTPAuthorizationCredentials
from fastapi import Depends,status,HTTPException
from pydantic import EmailStr


from ..schemas import user
from ..database import get_db
from sqlalchemy.orm import Session
from ..db_models.user import Users
from ..config import settings



oauth2_scheme=OAuth2PasswordBearer(tokenUrl='auth/login-2fa')

security=HTTPBearer()

#####Password Hashing and Verification

ph=PasswordHasher()

def hash_password(password:str)->str:
    return ph.hash(password)



def verify_password(plain_password:str,hashed_password:str)->bool:
    try:
        return ph.verify(hashed_password,plain_password)
    except VerifyMismatchError:
        return False



################################################################################################################################################
###2FA / TOTP Operations

def generate_totp_secret()->str:

    secret=pyotp.random_base32()
    return secret

def generate_qrcode_email(email:str,secret:str)->str:

    uri=pyotp.totp.TOTP(secret).provisioning_uri(name=email,issuer_name="BioShield AI")

    qr_image=qrcode.make(uri)

    buffer=io.BytesIO()
    qr_image.save(buffer,format='PNG')

    encoded_str=base64.b64encode(buffer.getvalue()).decode()

    return f"data:image/png;base64,{encoded_str}"

def generate_qrcode_phone(phone:str,secret:str)->str:

    uri=pyotp.totp.TOTP(secret).provisioning_uri(name=phone,issuer_name="BioShield AI")

    qr_image=qrcode.make(uri)

    buffer=io.BytesIO()
    qr_image.save(buffer,format='PNG')

    encoded_str=base64.b64encode(buffer.getvalue()).decode()

    return f"data:image/png;base64,{encoded_str}"

def verify_totp_code(secret:str,code:str)->bool:
    return pyotp.TOTP(secret).verify(code)





##############################################################################################################################################
####JWT Token Operations

SECRET_KEY=settings.SECRET_KEY
ALGORITHM=settings.ALGORITHM
EXPIRATION_TIME_MINUTES=settings.ACCESS_TOKEN_EXPIRE_MINUTES
TEMP_TOKEN_EXPIRE_MINUTES=settings.TEMP_TOKEN_EXPIRE_MINUTES



def create_temp_access_token(email:str):
    payload={'sub':email,'scope':'2fa_pending'}
    expire_at=datetime.now(timezone.utc)+timedelta(minutes=TEMP_TOKEN_EXPIRE_MINUTES)
    payload['exp']=expire_at

    temp_jwt=jwt.encode(payload,SECRET_KEY,ALGORITHM)
    return temp_jwt



def verify_temp_token(temp_jwt,credentials_exceptions=None):
    if credentials_exceptions is None:
        credentials_exceptions = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate temporary 2FA token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    try:

        temp_payload=jwt.decode(temp_jwt,SECRET_KEY,ALGORITHM)
        email:EmailStr=temp_payload.get('sub')
        if temp_payload.get('scope') != '2fa_pending':
            raise credentials_exceptions
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        token_data=user.TokenData(email=email)
        return token_data
    except JWTError:
        raise credentials_exceptions


def create_access_token(data:dict)->str:
    to_encode=data.copy()
    expire_at=datetime.now(timezone.utc)+timedelta(minutes=EXPIRATION_TIME_MINUTES)
    to_encode['exp']=expire_at

    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,ALGORITHM)
    return encoded_jwt

def decode_access_token(encoded_jwt,credentials_exceptions=None)->str:
    if credentials_exceptions is None:
        credentials_exceptions = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate temporary 2FA token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    try:
        payload=jwt.decode(encoded_jwt,SECRET_KEY,ALGORITHM)
        email:EmailStr=payload.get('sub')
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        token_data=user.TokenData(email=email)
        return token_data
    except JWTError:
        raise credentials_exceptions



def get_current_user_final(creds:HTTPAuthorizationCredentials=Depends(security),db:Session=Depends(get_db))->Users:
    credentials_exceptions=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='could not validate credentials',headers={'WWW-Authenticate':'Bearer'})
    token=creds.credentials
    token_data=decode_access_token(token,credentials_exceptions)

    user_info=db.query(Users).filter(Users.email==token_data.email).first()

    if user_info is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")

    return user_info