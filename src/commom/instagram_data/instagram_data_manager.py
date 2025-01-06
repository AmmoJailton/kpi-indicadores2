import time
from typing import Any, Callable, Dict, List
import pandas as pd
import datetime
import requests
from commom.database.data_handler import DataHandler
from commom.logger import logger
from commom.data_classes.instagram_data_class import SERVICE_NAME_LIST, IRequestInstagramParams, InstagramAccountInfo, Post
from commom.instagram_data.instagram_data_formater import InstagramDataFormater

class InstagramDataManager:
    services_availables: List[str]
    data_handler : DataHandler
    
    def __init__(self) -> None:
        self.services_availables = SERVICE_NAME_LIST
        self.data_handler = DataHandler()
    
    def fetch_accounts_infos(self, instagram_account_list: List[str]) -> List[InstagramAccountInfo]:
        current_service = self.services_availables[0]
        account_info: List[InstagramAccountInfo] = []
        logger.info(f"InstagramDataManager -> Fetching user info - init - {current_service}")
        
        for user in instagram_account_list:
            params: IRequestInstagramParams = InstagramDataFormater().get_service_params(service_name=current_service, username=user)
            headers: Dict[str, str] = InstagramDataFormater().format_params_to_headers(service_name=current_service, params=params)
            user_url: str = InstagramDataFormater().format_users_url(service_name=current_service, params=params)
            user_querystring: Dict[str, str] = InstagramDataFormater().format_user_querystring(service_name=current_service, params=params)
            
            try:
                logger.info(f"InstagramDataManager -> Get account info: {user}")
                response = requests.get(url=user_url, headers=headers, params=user_querystring)
                time.sleep(3)
           
            except Exception as e:
                logger.info(f"InstagramDataManager -> Failed to get info: {user}")
                logger.error(e)

            try:
                logger.info(f"InstagramDataManager -> Parse info: {user}")
                parsed_response:InstagramAccountInfo = InstagramDataFormater().parse_account_info(service_name=current_service, response=response.json())
                account_info.append(parsed_response)
            
            except Exception as e:
                logger.info(f"InstagramDataManager -> Parse failed for user: {user}")
                logger.info(f"InstagramDataManager -> Parse failed response: {response.json()}")
                logger.error(e)
                
                
        logger.info("InstagramDataManager -> Fetching user info - end")
        return account_info
    
    def _create_empty_accounts_history_dataset(self) -> pd.DataFrame:
        data = {}
        
        for column in InstagramAccountInfo.keys():
            data[column] = []
        
        return pd.DataFrame(data)
    
    def update_accounts_history_dataset(self, dataset: pd.DataFrame, account_info_list: List[InstagramAccountInfo]) -> pd.DataFrame:
        dataset['lastUpdate'] = pd.to_datetime(dataset['lastUpdate'], format="%Y-%m-%d", utc=True)
        df_empty = self._create_empty_accounts_history_dataset()
        today = pd.to_datetime('today', format="%Y-%m-%d", utc=True)
        month_init = pd.to_datetime(f'{today.year}-{today.month}-01', format="%Y-%m-%d", utc=True)
        init_month_mask = dataset['lastUpdate'] > month_init
        
        for account_info in account_info_list:
            df_account_info = account_info.to_dataframe()
            df_account_info['lastUpdate'] = pd.to_datetime(df_account_info['lastUpdate'], format="%Y-%m-%d", utc=True)
            username_mask = dataset['username'] == account_info.username
            df_current_month: pd.DataFrame = dataset[username_mask & init_month_mask].reset_index(drop=True)
            initial_count_mask = df_current_month['lastUpdate'] == df_current_month['lastUpdate'].min()
            
            if len(df_current_month[initial_count_mask]['followerCount']) < 1:
                initial_followers = account_info.followerCount
            else:
                initial_followers = df_current_month[initial_count_mask]['followerCount'].values[0]
            
            df_account_info['deltaBruto'] = account_info.followerCount - initial_followers
            df_account_info['deltaPorcentagem'] = (account_info.followerCount - initial_followers) / initial_followers
            df_empty = pd.concat([df_empty, df_account_info])

        dataset = dataset.reset_index(drop=True)
        df_updated = pd.concat([dataset, df_empty])
        return df_updated.reset_index(drop=True)
    
    def fetch_user_media_info(self, instagram_account_list: List[str]) -> Any:
        logger.info("InstagramDataManager -> Fetching posts - init")
        current_service = self.services_availables[0]
        posts_list: List[Post] = []
        logger.info(f"InstagramDataManager -> Service: {current_service}")
        
        for username in instagram_account_list:
            service_params = InstagramDataFormater().get_service_params(current_service, username)
            headers = InstagramDataFormater().format_params_to_headers(current_service, service_params)
            posts_url = InstagramDataFormater().format_media_url(current_service, service_params)
            media_querystring = InstagramDataFormater().format_media_querystring(current_service, service_params)
            logger.info(f"InstagramDataManager -> {username}")
            
            try:
                time.sleep(3)
                res = requests.get(url=posts_url, headers=headers, params=media_querystring)
                response = res.json()

            except Exception as e:
                logger.error(e)
                logger.info(f"InstagramDataManager -> Service not available: {current_service}")
            
            if response:
                try:
                    parsedResponse = InstagramDataFormater().parse_post_response(current_service, response)
                
                    for post in parsedResponse:
                        posts_list.append(post)
                
                except Exception as error:
                    logger.info('InstagramDataManager -> Error while parsing response')
                    logger.info(error)
            
        
        logger.info("InstagramDataManager -> Fetching posts - end")
        
        return posts_list

    def _create_empty_posts_dataset(self) -> pd.DataFrame:
        df = pd.DataFrame(columns=Post.keys())
        return df

    def update_posts_dataset(self, dataset: pd.DataFrame, posts_list: List[Post]) -> pd.DataFrame:
        logger.info("InstagramDataManager -> Update dataset - START")
        dataset['last_update'] = pd.to_datetime(dataset['last_update'], format="%Y-%m-%d", utc=True)
        df_temp = self._create_empty_posts_dataset()
        
        for post in posts_list:
            df_temp = pd.concat([df_temp, post.to_dataframe()])
        
        df_temp = df_temp.reset_index(drop=True)    
        
        dataset = pd.concat([dataset, df_temp])
        
        dataset = dataset.reset_index(drop=True)
        
        fillNaNColumnsDict = {
            "carousel_media_count": 0,
            "ig_play_count": 0,
            "play_count": 0,
            "share_count": 0,
            "video_duration": 0,
            "is_paid_partnership": False,
            "is_pinned": False,
            "did_report_as_spam": False,
            "carousel_media_ids": '[]'
        }
        
        dataset.fillna(fillNaNColumnsDict, inplace=True)
        dataset.drop_duplicates(subset=['code'], keep='first', inplace=True)
        
        logger.info("InstagramDataManager -> Update dataset - END")
        return dataset

    def load_current_account_history_dataset(self, source: str, **kwargs) -> pd.DataFrame:
        sources : Dict[str, Callable] = {
            "local": self.data_handler.read_from_local_pickle,
            "bigquery": self.data_handler.read_from_bigquery
        }

        try:
            dataframe : pd.DataFrame = sources[source](**kwargs)
            
        except:
            dataframe = self._create_empty_accounts_history_dataset()
        
        dataframe['lastUpdate'] = pd.to_datetime(dataframe['lastUpdate'])
        return dataframe.sort_values(by=['lastUpdate'], ascending=False)
    
    def save_current_account_history_dataset(self, source:str, **kwargs) -> bool:
        sources : Dict[str, Callable] = {
            "local": self.data_handler.write_to_pickle,
            "bigquery": self.data_handler.write_to_bigquery
        }
        
        try:
            sources[source](**kwargs)
        except:
            return False
        
        return True
    
    def get_usernames(self, dataset: pd.DataFrame) -> List[str]:
        return dataset['username'].unique().tolist()

    def get_last_update(self, dataset: pd.DataFrame) -> str:
        max_last_update = dataset['lastUpdate'].max()
        last_update = datetime.datetime.date(max_last_update)
        return last_update.strftime("%d-%m-%Y")