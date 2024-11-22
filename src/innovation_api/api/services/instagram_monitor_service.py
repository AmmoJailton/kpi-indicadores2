from typing import Any, List, Optional
import pandas as pd
from commom.database.queries.query_instagram_posts import QUERY_INSTAGRAM_POSTS
from commom.logger import logger
from commom.data_classes.instagram_data_class import InstagramAccountInfo
from commom.database.queries.query_instagram_monitor import QUERY_INSTAGRAM_MONITOR
from commom.instagram_data.instagram_data_manager import InstagramDataManager
from commom.report_generator import ReportGenerator
from innovation_messenger import IEmailProperties, Messenger


class InstagramMonitorService:
    data_manager : InstagramDataManager
    messenger: Messenger
    
    def __init__(self, messenger: Messenger) -> None:
        self.data_manager = InstagramDataManager()
        self.messenger = messenger
    
    def get_monitor_infos(self)-> Any:
        current_dataset = self.data_manager.load_current_account_history_dataset(source='bigquery', query=QUERY_INSTAGRAM_MONITOR)
        last_update = self.data_manager.get_last_update(current_dataset)
        usernames = self.data_manager.get_usernames(current_dataset)
        columns = current_dataset.columns.to_list()
        
        return {
            'result': 'Success',
            'data': {
                'last_update': last_update,
                'usernames': usernames,
                'columns': columns
            }
        }
        
    def update_accounts_info(self, usernames: List[str], debug_mode: bool) -> bool:
        logger.info(f"Update accounts - init")
        
        logger.info(f"Fetch accounts info from instagram via API ")
        users_info = self.data_manager.fetch_accounts_infos(instagram_account_list=usernames)
        
        if debug_mode:
            logger.info("Loading accounts info from Pickle")
            current_dataset = self.data_manager.load_current_account_history_dataset(source='local', file_path='accounts_info.pkl')
            
            logger.info("Updating accounts info")
            current_dataset = self.data_manager.update_accounts_history_dataset(dataset=current_dataset, account_info_list=users_info)
            
            logger.info("Saving accounts info to Pickle")
            self.data_manager.save_current_account_history_dataset(source='local', data=current_dataset, path='accounts_info.pkl')
            
        else:
            logger.info("Loading accounts info from BigQuery")
            current_dataset = self.data_manager.load_current_account_history_dataset(source='bigquery', query=QUERY_INSTAGRAM_MONITOR)
            
            logger.info("Updating accounts info")
            current_dataset = self.data_manager.update_accounts_history_dataset(dataset=current_dataset, account_info_list=users_info)
            
            logger.info("Saving accounts info to BigQuery")
            self.data_manager.save_current_account_history_dataset(source='bigquery', dataset_id='innovation_dataset', table_id='instagram_accounts_history', dataframe=current_dataset)
        
        return {
            'result': 'Success',
            'message': {
                'usernames': usernames,
                'updated_dataset': True
            }
        }
    
    def send_report_xlsx(self, recipients: List[str], debug_mode: bool, columns: Optional[List[str]] = None):
        logger.info("Send report - init")
        
        if columns is None:
            columns = ['last_update', 'username','name', 'follower_count', 'delta_bruto', 'delta_porcentagem']
        
        logger.info("Requested resources: " + str(columns))
        
        logger.info("Loading accounts info")
        if debug_mode:
            logger.info("Loading LOCAL FILE")
            current_dataset: pd.DataFrame = self.data_manager.load_current_account_history_dataset(source='local', file_path='accounts_info.pkl')
        else:
            logger.info("Loading BIGQUERY")
            current_dataset: pd.DataFrame = self.data_manager.load_current_account_history_dataset(source='bigquery', query=QUERY_INSTAGRAM_MONITOR)
        
        logger.info("Get last update  and usernames")
        last_update = self.data_manager.get_last_update(current_dataset)
        usernames = self.data_manager.get_usernames(current_dataset)
        
        logger.info("Format some data")
        current_dataset['delta_porcentagem'] = round(current_dataset['delta_porcentagem'], 4)
        current_dataset['last_update'] = current_dataset['last_update'].dt.strftime("%d-%m-%Y")
        filtered_dataset = current_dataset[columns].sort_values(by=['username','last_update'], ascending=True)
        
        logger.info("Generate report file and email properties")
        file_name = f'Seguidores_e_postagens_atualizado_{last_update}.xlsx'
        filtered_dataset.to_excel(file_name, sheet_name='Seguidores e postagens', index=False)

        email_body = f"""
        Report sobre número de seguidres e número total de postagens.
            
        Ultima atualização: {last_update}

        Contas observadas:
            {sorted(usernames).__str__().replace('[', '').replace(']', '').replace("'", "")}
        """
        
        email_subject = "[TESTE] - Seguidores e postagens - V0.0.2"
        email_properties = IEmailProperties(
            subject=email_subject,
            recipient=recipients,
            file_name=file_name,
            body=email_body
        )
        
        logger.info("Send email")
        
        self.messenger.send_message(
            channel='email',
            email_properties=email_properties
        )

        ReportGenerator().delete_report_file(file_name)

        logger.info("Send report - end")
        return {
            'result': 'Success',
            'message': {
                'recipients': recipients,
                'file_name': file_name,
                'email_subject': email_subject
            }
        }
    
    def update_posts(self, listOfUsernames, debugMode: bool = True):
        logger.info('SERVICE -> Updates posts - START')
        
        logger.info('SERVICE -> Get from API - START')
        postsList = self.data_manager.fetch_user_media_info(listOfUsernames)
        logger.info('SERVICE -> Get from API - END')
        
        if debugMode:
            logger.info('SERVICE -> DEBUG MODE')
            df_history : pd.DataFrame = pd.read_pickle('instagram_posts.pkl')
            
            datasetNew = self.data_manager.update_posts_dataset(df_history, postsList)
            
            self.data_manager.data_handler.write_to_pickle(datasetNew, 'instagram_posts.pkl')
        
        else:
            logger.info('SERVICE -> APPLICATION MODE')
            
            logger.info('SERVICE -> Read BQ')
            df_history = self.data_manager.data_handler.read_from_bigquery(query=QUERY_INSTAGRAM_POSTS)
            
            logger.info('SERVICE -> Update dataset with current + new posts')
            datasetNew = self.data_manager.update_posts_dataset(df_history, postsList)
            
            logger.info('SERVICE -> Write BQ')
            datasetNew = self.data_manager.data_handler.write_to_bigquery(dataset_id='innovation_dataset', table_id='instagram_posts', dataframe=datasetNew)
        
        logger.info('Updates posts - END')
        return datasetNew
    
    