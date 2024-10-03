from typing import Any, List
from commom.instagram_data.instagram_data_manager import InstagramDataManager


class InstagramMonitorService:
    data_manager : InstagramDataManager
    
    def __init__(self) -> None:
        self.data_manager = InstagramDataManager()
    
    def update_accounts_info(self, usernames: List[str]) -> Any:
        users_info = self.data_manager.fetch_user_info(list_of_users=usernames)
        current_dataset = self.data_manager.load_current_user_info_dataset()
        current_dataset = self.data_manager.populate_user_info_dataset(dataset=current_dataset, account_info_list=users_info)
        result = self.data_manager.save_current_user_info_dataset(dataset=current_dataset)
        return result
    
    def send_report_xlsx(self, recipients: List[str]) -> Any:
        current_dataset = self.data_manager.load_current_user_info_dataset()
        