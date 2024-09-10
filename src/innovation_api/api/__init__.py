from fastapi import APIRouter

from innovation_api.typing import IEndpoint


class Router:
    def __init__(self) -> None:
        self.router = APIRouter()

    def add_endpoint(self, endpoint: IEndpoint) -> None:
        for e in endpoint.endpoints:
            self.router.add_api_route(
                e.route, e.class_method, methods=[e.rest_method], tags=e.tags, responses=e.responses
            )
