from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import innovation_api
from innovation_api.api import Router
from innovation_api.api.controllers.daily_report_controller import DailyReportController
from innovation_api.api.controllers.instagram_monitor_controller import InstagramMonitorController
from innovation_api.api.controllers.login_artex_controller import LoginArtexController
from innovation_api.api.controllers.root_controller import RootController
from innovation_api.api.metadata.description import description, summary, title
from innovation_api.api.metadata.tags_metadata import tags_metadata
from innovation_messenger import Messenger


def create_api():
    messenger = Messenger()
    router = Router()
    
    fast_api = FastAPI(
        title=title,
        summary=summary,
        description=description,
        version=innovation_api.__version__,
        openapi_tags=tags_metadata,
    )
    fast_api.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    info_endpoint = RootController()
    daily_report_endpoint = DailyReportController(messenger=messenger)
    instagram_monitor_endpoint = InstagramMonitorController(messenger=messenger)
    login_artex_endpoint = LoginArtexController()
    
    endpoints = [
        info_endpoint, 
        daily_report_endpoint, 
        instagram_monitor_endpoint, 
        login_artex_endpoint
    ]

    for endpoint in endpoints:
        router.add_endpoint(endpoint)

    fast_api.include_router(router.router)

    return fast_api
