import datetime
import os
from typing import Any, Callable, Dict, List, Literal, Union
from commom.data_classes.instagram_data_class import IRequestInstagramParams, InstagramAccountInfo, InstagramCommentItem, InstagramCommentResponse, InstagramCommentResponseData, InstagramPostItem, InstagramPostResponseData, InstagramPostResponse, ServiceNames
import pandas as pd

class InstagramScrapperAPIDataFormater:
    def __init__(self) -> None:
        pass
    
    @classmethod
    def get_service_params(cls, username: str) -> IRequestInstagramParams:
        host = os.getenv("INSTAGRAM_SCRAPPER_API_HOST", 'instagram-scraper-api2.p.rapidapi.com')
        url = "https://" + host + "/"

        return IRequestInstagramParams(
            username=username,
            base_url=url,
            users_url="v1/info",
            posts_url="v1.2/posts",
            x_rapidapi_host=host,
            x_rapidapi_key=os.getenv("INSTAGRAM_SCRAPPER_API_TOKEN"),
            user_querystring="username_or_id_or_url",
            pagination_querystring="pagination_token",
            pagination_token=None
        )
    
    @classmethod
    def get_service_params_comments(cls, username: str, code_or_id_or_url: str) -> IRequestInstagramParams:
        host = os.getenv("INSTAGRAM_SCRAPPER_API_HOST", 'instagram-scraper-api2.p.rapidapi.com')
        url = "https://" + host + "/"

        return IRequestInstagramParams(
            username=username,
            base_url=url,
            users_url="v1/info",
            posts_url="v1.2/posts",
            comments_url="v1/comments",
            x_rapidapi_host=host,
            x_rapidapi_key=os.getenv("INSTAGRAM_SCRAPPER_API_TOKEN"),
            user_querystring="username_or_id_or_url",
            pagination_querystring="pagination_token",
            comments_querystring="code_or_id_or_url",
            post_code_id=code_or_id_or_url,
            pagination_token=None,  
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
    def format_posts_pagination_querystring(cls, params: IRequestInstagramParams) -> Dict[str, str]:
        return {
            params.user_querystring: params.username,
            params.pagination_querystring: params.pagination_token
        }
  
    @classmethod
    def format_comments_querystring(cls, params: IRequestInstagramParams) -> Dict[str, str]:
        return {
            params.comments_querystring: params.post_code_id,
            params.pagination_querystring: params.pagination_token
        }

    @classmethod
    def format_users_url(cls, params: IRequestInstagramParams) -> str:
        return params.base_url + params.users_url

    @classmethod
    def format_posts_url(cls, params: IRequestInstagramParams) -> str:
        return params.base_url + params.posts_url
    
    @classmethod
    def format_comments_url(cls, params: IRequestInstagramParams) -> str:
        return params.base_url + params.comments_url
    
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
    def parse_response_to_posts_obj(cls, response: Dict[str, Any]) -> InstagramPostResponse:
        data = dict(response['data'])
        pagination_token = response['pagination_token']
        count = data['count']
        items = list(data['items'])
        
        postItems:List[InstagramPostItem] = []
        
        for item in items:
            item = dict(item)
            caption = dict(item['caption'])
            if item.get('play_count', None) is None:
                item['play_count'] = 0
                
            postItems.append(
                InstagramPostItem(
                    created_at=datetime.datetime.fromtimestamp(caption['created_at_utc']).strftime("%d/%m/%Y"),
                    hashtags=caption.get('hashtags', []),
                    mentions=caption.get('mentions', []),
                    text=caption.get('text', ''),
                    code=item['code'],
                    comment_count=item.get('comment_count', 0),
                    id=item['id'],
                    like_and_view_counts_disabled=item['like_and_view_counts_disabled'],
                    like_count=item.get('like_count', 0),
                    media_name=item['media_name'],
                    media_type=item['media_type'],
                    play_count=item.get('play_count', None),
                    share_count=item.get('share_count', 0),
                    thumbnail_url=item['thumbnail_url'],
                    username=data['user']['username']
                )
            )
        
        responseData = InstagramPostResponse(
            data=InstagramPostResponseData(
                count=count,
                items=postItems
            ),
            pagination_token=pagination_token
        )
        
        return responseData

    @classmethod
    def parse_response_to_comments_obj(cls, response)->InstagramCommentResponse:
        data = dict(response['data'])
        pagination_token = response['pagination_token']
        count = data['count']
        total = data['total']
        items = list(data['items'])
        
        commentItems:List[InstagramCommentItem] = []
        
        for item in items:
            item = dict(item)
            user = dict(item['user'])
            
            commentItems.append(
                InstagramCommentItem(
                    created_at=datetime.datetime.fromtimestamp(item['created_at_utc']).strftime("%d/%m/%Y"),
                    comment_like_count=item.get('comment_like_count', 0),
                    spam=item.get('did_report_as_spam', False),
                    mentions=item.get('mentions', []),
                    text=item.get('text', ''),
                    comment_username=user.get('username', '')
                )
            )
            
        return InstagramCommentResponse(
            pagination_token=pagination_token,
            data=InstagramCommentResponseData(
                count=count,
                total=total,
                items=commentItems
            ),
        )


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
    def format_posts_pagination_querystring(cls, service_name: Union[str, ServiceNames], params: IRequestInstagramParams) -> Dict[str, str]:
        services_availables: Dict[str, Callable] = {
            "instagram_scrapper_api": InstagramScrapperAPIDataFormater().format_posts_pagination_querystring
        }
        
        return services_availables[service_name](params)

    @classmethod
    def format_users_url(cls, service_name: Union[str, ServiceNames], params: IRequestInstagramParams) -> str:
        services_availables: Dict[str, Callable] = {
            "instagram_scrapper_api": InstagramScrapperAPIDataFormater().format_users_url
        }
        
        return services_availables[service_name](params)

    @classmethod
    def format_posts_url(cls, service_name: Union[str, ServiceNames], params: IRequestInstagramParams) -> str:
        services_availables: Dict[str, Callable] = {
            "instagram_scrapper_api": InstagramScrapperAPIDataFormater().format_posts_url
        }
        
        return services_availables[service_name](params)

    @classmethod
    def parse_account_info(cls, service_name: str, response: Dict[str, Any]) -> InstagramAccountInfo:
        services_availables: Dict[str, Callable] = {
            "instagram_scrapper_api": InstagramScrapperAPIDataFormater().parse_account_info
        }
        
        return services_availables[service_name](response)
    
    @classmethod
    def parse_response_to_posts_obj(cls, service_name: str, response: Dict[str, Any]) -> InstagramPostResponse:
        services_availables: Dict[str, Callable] = {
            "instagram_scrapper_api": InstagramScrapperAPIDataFormater().parse_response_to_posts_obj
        }
        
        return services_availables[service_name](response)
    
    @classmethod
    def parse_response_to_comments_obj(cls, service_name: str, response: Dict[str, Any]) -> InstagramCommentResponse:
        services_availables: Dict[str, Callable] = {
            "instagram_scrapper_api": InstagramScrapperAPIDataFormater().parse_response_to_comments_obj
        }
        
        return services_availables[service_name](response)
