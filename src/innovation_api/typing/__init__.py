from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import Callable, List, Optional


@dataclass
class IEndpointConfig:
    route: str
    class_method: Callable
    rest_method: str
    tags: Optional[List[str]] = None
    responses: Optional[list] = None


class IEndpoint(metaclass=ABCMeta):
    @property
    @abstractmethod
    def endpoints(self) -> List[IEndpointConfig]:
        pass

    @abstractmethod
    def __init__(self) -> None:
        pass
