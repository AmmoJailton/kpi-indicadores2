from dataclasses import dataclass
import dataclasses
from typing import List, Literal, Optional, Union
import datetime
import pandas as pd
from pydantic import BaseModel

@dataclass
class InstagramCaptionInfo:
    text: str
    created_at_utc: Union[datetime.date, str, None]


@dataclass
class InstagramMediaInfo:
    instagram_code: str # api -> code
    caption: InstagramCaptionInfo
    comment_count: Union[int, str]
    like_count: Union[int, str]
    media_name: str
    share_count: Union[int, str]
    taken_at: Union[datetime.date, str, None]
    is_video: Optional[bool] = False
    play_count: Optional[Union[int, str]] = None
    carousel_media_count: Optional[Union[int, str]] = None
   
 
@dataclass
class InstagramAccountInfo:
    name: str # api -> full_name
    username: str
    follower_count: Union[int, str]
    total_media: Union[int, str]
    last_update: Union[datetime.date, str, None]
    biography: Optional[str] = None
    profile_pic: Optional[str] = None # api -> profile_pic_url_hd | profile_pic_url
    
    def asdict(self):
        return dataclasses.asdict(self)
    
    @property
    def keys(self):
        return self.asdict().keys

    def to_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame(self.asdict())

@dataclass
class IRequestInstagramParams:
    username: str
    base_url: str
    users_url: str
    posts_url: str
    x_rapidapi_key: str
    x_rapidapi_host: str
    user_querystring: str
    media_querystring: str
    pagination_token: Optional[str] = None

class UpdateInstagramAccountsInfoBody(BaseModel):
    usernames: List[str]

class SendInstagramAccountsInfoBody(BaseModel):
    recipients: List[str]
    debug_mode: Optional[bool] = True

ServiceNames = Literal[
    "instagram_scrapper_api"
]

SERVICE_NAME_LIST = [
    "instagram_scrapper_api"
]