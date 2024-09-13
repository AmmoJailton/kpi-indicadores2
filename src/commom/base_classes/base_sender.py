from abc import ABCMeta, abstractmethod


class BaseMessenger(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def send_message(self) -> None:
        pass
