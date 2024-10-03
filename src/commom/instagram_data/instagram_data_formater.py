import datetime
from typing import Any, Callable, Dict, List, Literal, Union
from commom.data_classes.instagram_data_class import IRequestInstagramParams, InstagramAccountInfo, ServiceNames, TrackedAccounts

class InstagramScrapperAPIDataFormater:
    def __init__(self) -> None:
        pass
    
    @classmethod
    def get_service_params(cls, username: TrackedAccounts) -> IRequestInstagramParams:
        return IRequestInstagramParams(
            username=username,
            base_url="https://instagram-scraper-api2.p.rapidapi.com/", # -> deve vir de uma ENV
            users_url="v1/info",
            posts_url="v1.2/posts",
            x_rapidapi_host="instagram-scraper-api2.p.rapidapi.com", # -> deve vir de uma ENV
            x_rapidapi_key="6f36805577msh5e42867c3bd4692p12525ajsn80e3751c2d32", # -> deve vir de uma ENV
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
            last_update=datetime.datetime.now().isoformat(),
            biography=data['biography'],
            profile_pic=data['profile_pic_url_hd']
        )


class InstagramDataFormater:
    scrapper_api: InstagramScrapperAPIDataFormater
    
    def __init__(self) -> None:
        self.scrapper_api = InstagramScrapperAPIDataFormater()
    
    @classmethod
    def get_service_params(cls, service_name: Union[str, ServiceNames], username: Union[str, TrackedAccounts]) -> IRequestInstagramParams:
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
