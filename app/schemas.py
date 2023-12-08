from pydantic import BaseModel, EmailStr, Json
from datetime import datetime
from typing import Optional, Any

from pydantic.types import conint


class UserOut(BaseModel):
	id: int
	email: EmailStr
	created_at: datetime

	class Config:
		from_attributes = True



class UserCreate(BaseModel):
    email: EmailStr
    password: str
    device_unique_id: str
    device_name: str
    device_type: str
    device_os: int
    device_mem: str

class UserLogin(BaseModel):
	email: EmailStr
	password: str


class Token(BaseModel):
	access_token: str
	token_type: str


class TokenData(BaseModel):
	id: Optional[str] = None


class ClientWeights(BaseModel):
    weights: Json



class aggregated_weights(BaseModel):
	aggregated_weight: Json


class the_global_model(BaseModel):
	model: Json


class ClientRequest(BaseModel):
    flag: int

