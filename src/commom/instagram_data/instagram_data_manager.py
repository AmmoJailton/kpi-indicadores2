import time
from typing import Any, Callable, Dict, List
import pandas as pd
import datetime
import requests
from commom.database.data_handler import DataHandler
from commom.logger import logger
from commom.data_classes.instagram_data_class import SERVICE_NAME_LIST, IRequestInstagramParams, InstagramAccountInfo
from commom.instagram_data.instagram_data_formater import InstagramDataFormater
import pickle

class InstagramDataManager:
    services_availables: List[str]
    data_handler : DataHandler
    
    def __init__(self) -> None:
        self.services_availables = SERVICE_NAME_LIST
        self.data_handler = DataHandler()
    
    def fetch_accounts_infos(self, instagram_account_list: List[str]) -> List[InstagramAccountInfo]:
        logger.info("Fetching user info - init")
        current_service = self.services_availables[0]
        account_info: List[InstagramAccountInfo] = []
        logger.info(f"Service: {current_service}")
        
        for user in instagram_account_list:
            params: IRequestInstagramParams = InstagramDataFormater().get_service_params(service_name=current_service, username=user)
            headers: Dict[str, str] = InstagramDataFormater().format_params_to_headers(service_name=current_service, params=params)
            user_url: str = InstagramDataFormater().format_users_url(service_name=current_service, params=params)
            user_querystring: Dict[str, str] = InstagramDataFormater().format_user_querystring(service_name=current_service, params=params)
            
            try:
                response = requests.get(url=user_url, headers=headers, params=user_querystring)
                parsed_response:InstagramAccountInfo = InstagramDataFormater().parse_account_info(service_name=current_service, response=response.json())
                account_info.append(parsed_response)
                time.sleep(1)
            except Exception as e:
                logger.info(f"Service not available: {current_service}")
                logger.error(e)
        logger.info("Fetching user info - end")
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
            initial_followers = df_current_month[initial_count_mask]['followerCount'].values[0]
            df_account_info['deltaBruto'] = account_info.followerCount - initial_followers
            df_account_info['deltaPorcentagem'] = (account_info.followerCount - initial_followers) / initial_followers
            df_empty = pd.concat([df_empty, df_account_info])

        dataset = dataset.reset_index(drop=True)
        df_updated = pd.concat([dataset, df_empty])
        return df_updated.reset_index(drop=True)
    
    def fetch_user_media_info(self, **kwargs) -> Any:
        return """
            TO BE IMPLEMENTED
        """
    
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
        max_lastUpdate = dataset['lastUpdate'].max()
        lastUpdate = datetime.datetime.date(max_lastUpdate)
        return lastUpdate.strftime("%d-%m-%Y")