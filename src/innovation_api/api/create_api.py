from fastapi import FastAPI

import innovation_api
from innovation_api.api import Router
from innovation_api.api.controllers.daily_report_controller import DailyReportController
from innovation_api.api.controllers.instagram_monitor_controller import InstagramMonitorController
from innovation_api.api.controllers.root_controller import RootController
from innovation_api.api.controllers.whatsapp_messenger_controller import WhatsappController
from innovation_api.api.metadata.description import description, summary, title
from innovation_api.api.metadata.tags_metadata import tags_metadata


def create_api():

    router = Router()
    fast_api = FastAPI(
        title=title,
        summary=summary,
        description=description,
        version=innovation_api.__version__,
        openapi_tags=tags_metadata,
    )

    info_endpoint = RootController()
    daily_report_endpoint = DailyReportController()
    whatsapp_messenger_endpoint = WhatsappController()
    instagram_monitor_endpoint = InstagramMonitorController()
    
    endpoints = [info_endpoint, daily_report_endpoint, instagram_monitor_endpoint]

    for endpoint in endpoints:
        router.add_endpoint(endpoint)

    fast_api.include_router(router.router)

    return fast_api
