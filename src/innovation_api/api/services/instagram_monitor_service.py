from typing import Any, List
from commom.instagram_data.instagram_data_manager import InstagramDataManager
from commom.report_generator import ReportGenerator
from innovation_messenger import IEmailProperties, Messenger


class InstagramMonitorService:
    data_manager : InstagramDataManager
    messenger: Messenger
    
    def __init__(self) -> None:
        self.data_manager = InstagramDataManager()
        self.messenger = Messenger()
    
    def update_accounts_info(self, usernames: List[str]) -> Any:
        users_info = self.data_manager.fetch_user_info(list_of_users=usernames)
        current_dataset = self.data_manager.load_current_user_info_dataset()
        current_dataset = self.data_manager.populate_user_info_dataset(dataset=current_dataset, account_info_list=users_info)
        result = self.data_manager.save_current_user_info_dataset(dataset=current_dataset)
        return result
    
    def send_report_xlsx(self, recipients: List[str]) -> Any:
        file_name = 'Seguidores_e_postagens.xlsx'

        current_dataset = self.data_manager.load_current_user_info_dataset()
        current_dataset.to_excel(file_name, sheet_name='Seguidores e postagens', index=False)

        email_body = """
            Report sobre número de seguidres e número total de postagens.
        """
        email_subject = "[TESTE] - Seguidores e postagens"
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

        return True
    