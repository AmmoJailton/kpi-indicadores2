from dataclasses import dataclass
import dataclasses
from typing import List, Literal, Optional, Union, Any
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
    
    def to_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame(self.asdict(), index=[0])

    def keys():
        return InstagramAccountInfo.__dataclass_fields__.keys()

@dataclass
class Post:
    code: str
    comment_count: int
    is_pinned: bool
    is_video: bool
    like_and_view_counts_disabled: bool
    like_count: int
    media_name: str
    share_count: int
    user_id: Union[int, str]
    username: str
    created_at_utc: Union[int, str, Any]
    id: Union[int, str]
    last_update: Union[datetime.datetime,datetime.date, str]
    text: Optional[str] = ''
    ig_play_count: Optional[int] = 0
    is_paid_partnership: Optional[bool] = False
    play_count: Optional[int] = 0
    did_report_as_spam: Optional[bool] = False
    hashtags: Optional[Any] = None
    mentions: Optional[Any] = None
    video_duration: Optional[Any] = None
    carousel_media_count: Optional[int] = None
    carousel_media_ids: Optional[Any] = None
    
    def asdict(self):
        return dataclasses.asdict(self)
    
    def to_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame(data=self.asdict(), columns=self.asdict().keys(), index=[0])
    
    def keys():
        return Post.__dataclass_fields__.keys()

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
    debug_mode: Optional[bool] = True
    
class SendInstagramAccountsInfoBody(BaseModel):
    recipients: List[str]
    columns: Optional[List[str]] = None
    debug_mode: Optional[bool] = True

ServiceNames = Literal[
    "instagram_scrapper_api"
]

SERVICE_NAME_LIST = [
    "instagram_scrapper_api"
]