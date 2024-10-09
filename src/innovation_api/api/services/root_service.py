import datetime
import os
from typing import List
from innovation_api.typing import IEndpoint, IEndpointConfig
from innovation_api import __version__

class RootService():
    def __init__(self):
        pass

    def get_info(self):
        now = datetime.datetime.now()
        return {
            "statusCode": 201,
            "version": __version__,
            "env": os.getenv("ENV"),
            "Status": f"{now}",
        }
