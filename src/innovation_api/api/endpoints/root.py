import datetime
import os
from typing import List

from innovation_api import __version__
from innovation_api.typing import IEndpoint, IEndpointConfig


class RootEndpoint(IEndpoint):
    @property
    def endpoints(self) -> List[IEndpointConfig]:
        return [IEndpointConfig(route="/", class_method=self.get_info, rest_method="GET", tags=["Get Info"])]

    def __init__(self) -> None:
        pass

    def get_info(self):
        now = datetime.datetime.now()
        return {
            "statusCode": 201,
            "version": __version__,
            "env": os.getenv("ENV"),
            "Status": f"A requisição foi feita em: {now}",
        }


class TestEndpoint(IEndpoint):
    @property
    def endpoints(self) -> List[IEndpointConfig]:
        return [IEndpointConfig(route="/test", class_method=self.get_info, rest_method="GET", tags=["Get Info"])]

    def __init__(self) -> None:
        pass

    def get_info(self):
        return {"statusCode": 201, "version": __version__, "env": os.getenv("ENV"), "test": "endpoint de teste"}
