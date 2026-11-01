from pydantic import BaseModel,EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumberValidator
from typing import Optional,Annotated,Union
import phonenumbers
from datetime import datetime


E164phonenumber=Annotated[Union[str,phonenumbers.PhoneNumber],PhoneNumberValidator(default_region='IN',number_format='E164')]

class UserRegister(BaseModel):
    name:str
    email:EmailStr
    password:str
    phonenumber:E164phonenumber


class UserRegisterResponse(BaseModel):
    email:EmailStr
    secret:str
    qr_code_base64:str


class Verify2FASetup(BaseModel):
    email:Optional[EmailStr]=None
    phonenumber:Optional[E164phonenumber]=None
    otp:str

class UserLogin(BaseModel):
    email:Optional[EmailStr]=None
    password:str
    phonenumber:Optional[E164phonenumber]=None

class LoginResponse(BaseModel):
    status:str
    message:Optional[str]=None
    temp_token:Optional[str]=None
    access_token:Optional[str]=None
    token_type:Optional[str]=None
    qr_code:Optional[str]=None



class Verify2FALogin(BaseModel):
    temp_token:str
    code:str

class TokenData(BaseModel):
    email:EmailStr


