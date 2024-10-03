from typing import Any, Dict, List

from fastapi import HTTPException
from commom.data_classes.report_content_data_class import DailyReportBody, DebugBody
from innovation_api.api.services.daily_report_service import DailyReportService
from innovation_api.typing import IEndpoint, IEndpointConfig

class DailyReportController(IEndpoint):
    TAGS = ["KPI report"]
    daily_report_service: DailyReportService

    @property
    def endpoints(self) -> List[IEndpointConfig]:
        return [
            IEndpointConfig(
                route="/dailyreport", class_method=self.send_kpi_daily_mail, rest_method="POST", tags=self.TAGS
            ),
            IEndpointConfig(
                route="/dailyreport-all",
                class_method=self.send_kpi_daily_mail_all,
                rest_method="POST",
                tags=self.TAGS,
            ),
        ]

    def __init__(self) -> None:
        self.daily_report_service = DailyReportService()
        pass

    def send_kpi_daily_mail(self, body: DailyReportBody) -> Dict[str, Any]:
        if len(body.ids_loja) < 1:
            raise HTTPException(status_code=400, detail="Invalid ids_loja")
        
        return self.daily_report_service.send_kpi_daily_mail(body= body)
        

    def send_kpi_daily_mail_all(self, body: DebugBody):
        return self.daily_report_service.send_kpi_daily_mail_all(body=body)
