import time
from typing import Any, Dict, List
import pandas as pd
import datetime
import requests
from commom.data_classes.instagram_data_class import SERVICE_NAME_LIST, IRequestInstagramParams, InstagramAccountInfo
from commom.instagram_data.instagram_data_formater import InstagramDataFormater
import pickle

class InstagramDataManager:
    services_availables: List[str]
    
    def __init__(self) -> None:
        self.services_availables = SERVICE_NAME_LIST
    
    def fetch_user_info(self, list_of_users: List[str]) -> List[InstagramAccountInfo]:
        current_service = self.services_availables[0]
        account_info: List[InstagramAccountInfo] = []
        
        for user in list_of_users:
            params: IRequestInstagramParams = InstagramDataFormater().get_service_params(service_name=current_service, username=user)
            headers: Dict[str, str] = InstagramDataFormater().format_params_to_headers(service_name=current_service, params=params)
            user_url: str = InstagramDataFormater().format_users_url(service_name=current_service, params=params)
            user_querystring: Dict[str, str] = InstagramDataFormater().format_user_querystring(service_name=current_service, params=params)
            
            # if request fail we have to try another service
            response = requests.get(url=user_url, headers=headers, params=user_querystring)
            time.sleep(1)
            # 
            parsed_response:InstagramAccountInfo = InstagramDataFormater().parse_account_info(service_name=current_service, response=response.json())
            account_info.append(parsed_response)
        
        return account_info
    
    def _create_empty_user_info_dataset(self) -> pd.DataFrame:
        data = {}
        for column in InstagramAccountInfo.__dataclass_fields__.keys():
            data[column] = []
        
        return pd.DataFrame(data)
    
    def update_user_info_dataset(self, dataset: pd.DataFrame, account_info_list: List[InstagramAccountInfo]) -> pd.DataFrame:
        df_info_list = [account_info.to_dataframe() for account_info in account_info_list]
        updated_df = pd.concat(df_info_list+[dataset]).sort_values(by=['last_update', 'username'], ascending=False)
        return updated_df
    # def update_user_info_dataset(self, dataset: pd.DataFrame, account_info_list: List[InstagramAccountInfo]) -> pd.DataFrame:
    #     df_user_info = dataset
        
    #     for account_info in account_info_list:
    #         value = []
    #         user = InstagramAccountInfo.keys
            
    #         for k in user:
    #             value.append(user[k])

    #         value = pd.Series(value)
            
    #         df_user_info = df_user_info._append(dict(zip(dataset.columns, value)), ignore_index=True)
        
    #     return df_user_info
    
    def fetch_user_media_info(self, **kwargs) -> Any:
        return """
            TO BE IMPLEMENTED
        """
    
    def load_current_user_info_dataset(self) -> pd.DataFrame:
        try:
        # buscar os dados no BQ
            dataframe : pd.DataFrame = pickle.load(open("accounts_info.pkl", "rb"))
        #### se os dados no BQ estiverem vazios
        # if data is empty:
        #    dataframe = self._create_empty_user_info_dataset()
        except:
            dataframe = self._create_empty_user_info_dataset()
        
        return dataframe.sort_values(by='last_update', ascending=False)
    
    def save_current_user_info_dataset(self, dataset: pd.DataFrame) -> bool:
        # salvar os dados no BQ
        pickle.dump(dataset, open("accounts_info.pkl", "wb"))
        print(dataset)
        return True
    
    def get_usernames(self, dataset: pd.DataFrame) -> List[str]:
        return dataset['username'].unique().tolist()

    def get_last_update(self, dataset: pd.DataFrame) -> str:
        max_last_update = dataset['last_update'].max()
        last_update = datetime.datetime.fromisoformat(max_last_update)
        return last_update.strftime("%d-%m-%Y")