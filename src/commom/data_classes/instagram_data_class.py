from dataclasses import dataclass
import dataclasses
from typing import Any, List, Literal, Optional, Union
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
class IRequestInstagramParams:
    username: str
    base_url: str
    users_url: str
    posts_url: str
    x_rapidapi_key: str
    x_rapidapi_host: str
    user_querystring: str
    pagination_querystring: str
    pagination_token: Optional[str] = None
    comments_url: Optional[str] = None
    comments_querystring: Optional[str] = None
    post_code_id: Optional[str] = None


@dataclass
class InstagramPostItem:
    created_at: Union[int, str, Any]
    hashtags: List[str]
    mentions: List[str]
    text: Union[str, Any]
    code: Union[Any, str]
    comment_count: int
    id: Union[int, str]
    like_and_view_counts_disabled: bool
    like_count: int
    media_name: str
    media_type: int
    play_count: int
    thumbnail_url: Union[str, Any]
    share_count: int
    username: str

@dataclass
class InstagramPostResponseData:
    count: int
    items: List[InstagramPostItem]

@dataclass
class InstagramPostResponse:
    data: InstagramPostResponseData
    pagination_token: str

@dataclass
class InstagramCommentItem:
    created_at: Union[str, datetime.date, datetime.datetime, Any] 
    comment_like_count: int
    spam: bool
    mentions: List[str]
    text: str
    comment_username: str

@dataclass
class InstagramCommentResponseData:
    count: int
    total: int
    items: List[InstagramCommentItem]

@dataclass
class InstagramCommentResponse:
    data: InstagramCommentResponseData
    pagination_token: str


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
