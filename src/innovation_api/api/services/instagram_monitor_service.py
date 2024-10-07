from typing import List
import pandas as pd
from commom.database.queries.query_instagram_monitor import QUERY_INSTAGRAM_MONITOR
from commom.instagram_data.instagram_data_manager import InstagramDataManager
from commom.report_generator import ReportGenerator
from innovation_messenger import IEmailProperties, Messenger


class InstagramMonitorService:
    data_manager : InstagramDataManager
    messenger: Messenger
    
    def __init__(self) -> None:
        self.data_manager = InstagramDataManager()
        self.messenger = Messenger()
    
    def update_accounts_info(self, usernames: List[str], debug_mode: bool) -> bool:
        users_info = self.data_manager.fetch_accounts_infos(instagram_account_list=usernames)
        
        if debug_mode:
            current_dataset = self.data_manager.load_current_account_history_dataset('local', 'accounts_info.pkl')
            current_dataset = self.data_manager.update_accounts_history_dataset(dataset=current_dataset, account_info_list=users_info)
            result = self.data_manager.save_current_account_history_dataset(source='local', data=current_dataset, path='accounts_info.pkl')
        else:
            current_dataset = self.data_manager.load_current_account_history_dataset('bigquery', QUERY_INSTAGRAM_MONITOR)
            current_dataset = self.data_manager.update_accounts_history_dataset(dataset=current_dataset, account_info_list=users_info)
            result = self.data_manager.save_current_account_history_dataset(source='bigquery', dataset_id='innovation_dataset', table_id='instagram_accounts_history', dataframe=current_dataset)
        
        return result
    
    def send_report_xlsx(self, recipients: List[str], debug_mode: bool):

        if debug_mode:
            current_dataset: pd.DataFrame = self.data_manager.load_current_account_history_dataset(source='local', file_path='accounts_info.pkl')
        else:
            current_dataset: pd.DataFrame = self.data_manager.load_current_account_history_dataset(source='bigquery', query=QUERY_INSTAGRAM_MONITOR)
        
        last_update = self.data_manager.get_last_update(current_dataset)
        usernames = self.data_manager.get_usernames(current_dataset)
        
        file_name = f'Seguidores_e_postagens_atualizado_{last_update}.xlsx'
        
        current_dataset.to_excel(file_name, sheet_name='Seguidores e postagens', index=False)

        email_body = f"""
            Report sobre número de seguidres e número total de postagens.
            
            Ultima atualização: {last_update}
            
            Contas observadas: 
            {sorted(usernames).__str__().replace('[', '').replace(']', '').replace("'", "")}
        """
        
        email_subject = "[TESTE] - Seguidores e postagens - V0.0.1.alpha"
        email_properties = IEmailProperties(
            subject=email_subject,
            recipient=recipients,
            file_name=file_name,
            body=email_body
        )
        
        self.messenger.send_message(
            channel='email',
            email_properties=email_properties
        )
        ReportGenerator().delete_report_file(file_name)

        return email_body
    