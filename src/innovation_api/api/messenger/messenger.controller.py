
class RootEndpoint(IEndpoint):
    @property
    def endpoints(self) -> List[IEndpointConfig]:
        return [IEndpointConfig(route="/", class_method=messenger.service.getInfo, rest_method="GET", tags=["Get Info"])]

    def __init__(self) -> None:
        pass


