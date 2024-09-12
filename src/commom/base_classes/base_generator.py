from abc import ABCMeta, abstractmethod


class BaseGenerator(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def generate_report(self) -> None:
        pass

    @abstractmethod
    def format_report_content(self) -> None:
        pass

    @abstractmethod
    def get_recipients_for_report(self) -> None:
        pass
