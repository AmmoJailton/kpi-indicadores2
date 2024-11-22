import datetime
import os
from typing import Any, Callable, Dict, List, Literal, Union
from commom.data_classes.instagram_data_class import IRequestInstagramParams, InstagramAccountInfo, Post, ServiceNames
import pandas as pd

class InstagramScrapperAPIDataFormater:
    def __init__(self) -> None:
        pass
    
    @classmethod
    def get_service_params(cls, username: str) -> IRequestInstagramParams:
        host = 'instagram-scraper-api2.p.rapidapi.com'
        # host = os.getenv("INSTAGRAM_SCRAPPER_API_HOST")
        url = "https://" + host + "/"

        return IRequestInstagramParams(
            username=username,
            base_url=url,
            users_url="v1/info",
            posts_url="v1.2/posts",
            x_rapidapi_host=host,
            x_rapidapi_key="6f36805577msh5e42867c3bd4692p12525ajsn80e3751c2d32",
            # x_rapidapi_key=os.getenv("INSTAGRAM_SCRAPPER_API_TOKEN"),
            user_querystring="username_or_id_or_url",
            media_querystring="pagination_token",
            pagination_token=None
        )
    
    @classmethod
    def format_params_to_headers(cls, params: IRequestInstagramParams) -> Dict[str, str]:
        return {
            "x-rapidapi-host": params.x_rapidapi_host,
            "x-rapidapi-key": params.x_rapidapi_key
        }
    
    @classmethod
    def format_user_querystring(cls, params: IRequestInstagramParams) -> Dict[str, str]:
        return {
            params.user_querystring: params.username
        }

    @classmethod
    def format_media_querystring(cls, params: IRequestInstagramParams) -> Dict[str, str]:
        return {
            params.user_querystring: params.username,
            params.media_querystring: params.pagination_token
        }

    @classmethod
    def format_users_url(cls, params: IRequestInstagramParams) -> str:
        return params.base_url + params.users_url

    @classmethod
    def format_media_url(cls, params: IRequestInstagramParams) -> str:
        return params.base_url + params.posts_url
    
    @classmethod
    def parse_account_info(cls, response) -> InstagramAccountInfo:
        data = response['data']
        
        return InstagramAccountInfo(
            name=data['full_name'],
            username=data['username'],
            follower_count=data['follower_count'],
            total_media=data['media_count'],
            last_update=pd.to_datetime('today', format="%Y-%m-%d", utc=True),
            biography=data['biography'],
            profile_pic=data['profile_pic_url_hd']
        )
    
    @classmethod
    def parse_post_response(cls, jsonObj) -> List[Post]:
        postsList : List[Post] = []
        
        data = jsonObj['data']
        items = data["items"]
        count = data["count"]
        
        if count > 0:
            for item in items:
                caption = item['caption']
                user = item["user"]
                carousel_media_ids = '[]'
                is_paid_partnership = False
                is_pinned = False
                carousel_media_count = 0
                ig_play_count = 0
                play_count = 0
                share_count = 0
                video_duration = 0
                
                if 'carousel_media_count' in item.keys():
                    carousel_media_count = item['carousel_media_count']
                    carousel_media_ids = str(item['carousel_media_ids'])
                
                if 'is_paid_partnership' in item.keys():
                    is_paid_partnership = item['is_paid_partnership']
                
                if 'ig_play_count' in item.keys():
                    ig_play_count = item['ig_play_count']
                    play_count = item['play_count']
                
                if 'share_count' in item.keys():
                    share_count = item['share_count']
                
                if 'video_duration' in item.keys():
                    video_duration = item['video_duration']
                
                if 'is_pinned' in item.keys():
                    is_pinned = item['is_pinned']
                    
                post = Post(
                    code= item['code'],
                    comment_count= item['comment_count'],
                    ig_play_count= ig_play_count,
                    play_count= play_count,
                    is_paid_partnership = is_paid_partnership,
                    is_pinned= is_pinned,
                    is_video= item['is_video'],
                    like_and_view_counts_disabled= item['like_and_view_counts_disabled'],
                    like_count= item['like_count'],
                    media_name= item['media_name'],
                    share_count= share_count,
                    user_id= user['id'],
                    username= user['username'],
                    created_at_utc= caption['created_at_utc'],
                    id= caption['id'],
                    text= caption['text'],
                    did_report_as_spam= caption['did_report_as_spam'],
                    hashtags= str(caption['hashtags']),
                    mentions= str(caption['mentions']),
                    video_duration= video_duration,
                    carousel_media_count= carousel_media_count,
                    carousel_media_ids= carousel_media_ids,
                    last_update= pd.to_datetime('today', format="%Y-%m-%d", utc=True),
                )
                postsList.append(post)
        
        return postsList

class InstagramDataFormater:
    scrapper_api: InstagramScrapperAPIDataFormater
    
    def __init__(self) -> None:
        self.scrapper_api = InstagramScrapperAPIDataFormater()
    
    @classmethod
    def get_service_params(cls, service_name: Union[str, ServiceNames], username: Union[str, Any]) -> IRequestInstagramParams:
        services_availables: Dict[str, Callable] = {
            "instagram_scrapper_api": InstagramScrapperAPIDataFormater().get_service_params
        }
        
        return services_availables[service_name](username)
    
    @classmethod
    def format_params_to_headers(cls, service_name: Union[str, ServiceNames], params: IRequestInstagramParams) -> Dict[str, str]:
        services_availables: Dict[str, Callable] = {
            "instagram_scrapper_api": InstagramScrapperAPIDataFormater().format_params_to_headers
        }
        
        return services_availables[service_name](params)
    
    @classmethod
    def format_user_querystring(cls, service_name: Union[str, ServiceNames], params: IRequestInstagramParams) -> Dict[str, str]:
        services_availables: Dict[str, Callable] = {
            "instagram_scrapper_api": InstagramScrapperAPIDataFormater().format_user_querystring
        }
        
        return services_availables[service_name](params)

    @classmethod
    def format_media_querystring(cls, service_name: Union[str, ServiceNames], params: IRequestInstagramParams) -> Dict[str, str]:
        services_availables: Dict[str, Callable] = {
            "instagram_scrapper_api": InstagramScrapperAPIDataFormater().format_media_querystring
        }
        
        return services_availables[service_name](params)

    @classmethod
    def format_users_url(cls, service_name: Union[str, ServiceNames], params: IRequestInstagramParams) -> str:
        services_availables: Dict[str, Callable] = {
            "instagram_scrapper_api": InstagramScrapperAPIDataFormater().format_users_url
        }
        
        return services_availables[service_name](params)

    @classmethod
    def format_media_url(cls, service_name: Union[str, ServiceNames], params: IRequestInstagramParams) -> str:
        services_availables: Dict[str, Callable] = {
            "instagram_scrapper_api": InstagramScrapperAPIDataFormater().format_media_url
        }
        
        return services_availables[service_name](params)

    @classmethod
    def parse_account_info(cls, service_name: str, response: Dict[str, Any]) -> InstagramAccountInfo:
        services_availables: Dict[str, Callable] = {
            "instagram_scrapper_api": InstagramScrapperAPIDataFormater().parse_account_info
        }
        
        return services_availables[service_name](response)
    
    @classmethod
    def parse_post_response(cls, service_name: str, response: Dict[str, Any]) -> InstagramAccountInfo:
        services_availables: Dict[str, Callable] = {
            "instagram_scrapper_api": InstagramScrapperAPIDataFormater().parse_post_response
        }
        
        return services_availables[service_name](response)
