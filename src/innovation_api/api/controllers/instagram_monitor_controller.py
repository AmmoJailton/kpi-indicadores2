from typing import Any, List
from commom.data_classes.instagram_data_class import UpdateInstagramAccountsInfoBody, SendInstagramAccountsInfoBody
from innovation_api.api.services.instagram_monitor_service import InstagramMonitorService
from innovation_api.typing import IEndpoint, IEndpointConfig


class InstagramMonitorController(IEndpoint):
    TAGS = ["Instagram monitor"]
    instagram_service: InstagramMonitorService
    
    @property
    def endpoints(self) -> List[IEndpointConfig]:
        return [
            IEndpointConfig(
                route="/update-accounts-info",
                rest_method="POST",
                class_method=self.update_accounts_info,
                tags=self.TAGS
            ),
            IEndpointConfig(
                route="/send-report-xlsx",
                rest_method="POST",
                class_method=self.send_report_xlsx,
                tags=self.TAGS
            )
        ]

    def __init__(self) -> None:
        self.instagram_service = InstagramMonitorService()

    def update_accounts_info(self, body: UpdateInstagramAccountsInfoBody) -> Any:
        usernames = body.usernames
        if len(usernames) < 1:
            return False

        result = self.instagram_service.update_accounts_info(usernames)
        return result
    
    def send_report_xlsx(self, body: SendInstagramAccountsInfoBody) -> bool:
        recipients = body.recipients
        debug_mode = body.debug_mode
        
        if len(recipients) < 1:
            return False
        
        result = self.instagram_service.send_report_xlsx(recipients)
        return result