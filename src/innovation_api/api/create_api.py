from fastapi import FastAPI

import innovation_api
from innovation_api.api import Router
from innovation_api.api.endpoints.root import RootEndpoint, TestEndpoint
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

    info_endpoint = RootEndpoint()
    outro_info = TestEndpoint()

    endpoints = [info_endpoint, outro_info]

    for endpoint in endpoints:
        router.add_endpoint(endpoint)

    fast_api.include_router(router.router)

    return fast_api
