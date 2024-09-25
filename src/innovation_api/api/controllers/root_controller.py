import datetime
import os
from typing import List
from innovation_api.api.services.root_service import RootService
from innovation_api.typing import IEndpoint, IEndpointConfig
from innovation_api import __version__

class RootController(IEndpoint):
    root_service : RootService
    
    @property
    def endpoints(self) -> List[IEndpointConfig]: 
        return [IEndpointConfig(route="/", class_method=self.get_info, rest_method="GET", tags=["Get Info"])]

    def __init__(self) -> None:
        self.root_service = RootService()
        pass

    def get_info(self):
        return self.root_service.get_info()
