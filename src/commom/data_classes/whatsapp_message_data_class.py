from dataclasses import dataclass
from typing import Any, Dict, List, Literal, Optional, Union

from pydantic import BaseModel
MediaTypes = Literal['image', 'jpeg']

@dataclass
class IWhastappMessageButtons(BaseModel):
    label: str
    intentIdOrName:str
    webhookPayload:str
    description:str

@dataclass
class IWhastappMessageMedia(BaseModel):
    mimeType: Union[MediaTypes, str]
    url: str

@dataclass
class IWhastappMessageLocation(BaseModel):
    latitude: str
    longitude: str
    name: str
    address: str

@dataclass
class IWhastappMessageContact(BaseModel):
    firstName: str
    middleName: str
    lastName: str
    emails: List[str]
    phones: List[str]
    
@dataclass
class IWhatsappMessage(BaseModel):
    text: Optional[str] = None
    buttons: Optional[List[IWhastappMessageButtons]] = None
    media: Optional[List[IWhastappMessageMedia]] = None
    location: Optional[List[IWhastappMessageLocation]] = None
    contact: Optional[IWhastappMessageContact] = None
    webhookPayload: Optional[str] = None
    
@dataclass
class IWhatsappBody(BaseModel):
    phone: str
    message: Optional[IWhatsappMessage] = None