from typing import Any, List
from commom.data_classes.instagram_data_class import UpdateInstagramAccountsInfoBody, SendInstagramAccountsInfoBody
from innovation_api.api.services.instagram_monitor_service import InstagramMonitorService
from innovation_api.typing import IEndpoint, IEndpointConfig
from innovation_messenger import Messenger


class InstagramMonitorController(IEndpoint):
    TAGS = ["Instagram monitor"]
    instagram_service: InstagramMonitorService
    
    @property
    def endpoints(self) -> List[IEndpointConfig]:
        return [
            IEndpointConfig(
                route="/instagram-monitor/update-accounts-info",
                rest_method="POST",
                class_method=self.update_accounts_info,
                tags=self.TAGS
            ),
            IEndpointConfig(
                route="/instagram-monitor/send-report-xlsx",
                rest_method="POST",
                class_method=self.send_report_xlsx,
                tags=self.TAGS
            )
        ]

    def __init__(self, messenger: Messenger) -> None:
        self.instagram_service = InstagramMonitorService(messenger=messenger)

    def update_accounts_info(self, body: UpdateInstagramAccountsInfoBody) -> Any:
        usernames = body.usernames
        if len(usernames) < 1:
            return {
                'result': 'Error',
                'message': 'Invalid usernames'
            }
        
        try:
            result = self.instagram_service.update_accounts_info(usernames, body.debug_mode)
        except Exception as e:
            result = {
                'result': 'Error',
                'message': 'Error while updating accounts info',
                'exception': str(e)
            }
        
        return result
    
    def send_report_xlsx(self, body: SendInstagramAccountsInfoBody) -> Any:
        recipients = body.recipients
        
        if len(recipients) < 1:
            return {
                'result': 'Error',
                'message': 'Invalid recipients'
            }
        
        try:
            result = self.instagram_service.send_report_xlsx(recipients, body.debug_mode)
        except Exception as e:
            result = {
                'result': 'Error',
                'message': 'Error while sending report',
                'exception': str(e)
            }
            
        return result