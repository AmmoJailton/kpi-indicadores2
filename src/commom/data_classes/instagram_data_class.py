from dataclasses import dataclass
from typing import List, Literal, Optional, Union
import datetime

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


# Isso está aqui por falta de um lugar melhor e para evitar dependências circulares
# Não sei se isso será necessário
# Parece redundante
TrackedAccounts = Literal[
    "altenburg.oficial",
    "altenburghaus",
    "artelasse",
    "artex",
    "buddemeyeroficial",
    "casaalmeidaoficial",
    "casariachuelo",
    "casa.sonno",
    "hoomybr",
    "karstenoficial",
    "mmartanoficial",
    "santistadecora",
    "trussardioficial",
    "trousseauoficial",
    "zeloloja"
]

TRACKED_ACCOUNT_LIST = [
    "altenburg.oficial",
    "altenburghaus",
    "artelasse",
    "artex",
    "buddemeyeroficial",
    "casaalmeidaoficial",
    "casariachuelo",
    "casa.sonno",
    "hoomybr",
    "karstenoficial",
    "mmartanoficial",
    "santistadecora",
    "trussardioficial",
    "trousseauoficial",
    "zeloloja"
]

ServiceNames = Literal[
    "instagram_scrapper_api"
]

SERVICE_NAME_LIST = [
    "instagram_scrapper_api"
]