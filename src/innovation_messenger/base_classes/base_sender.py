from abc import ABCMeta, abstractmethod

class BaseSender(metaclass=ABCMeta):

  @abstractmethod
  def __init__(self) -> None:
    pass

  @abstractmethod
  def send_report(self) -> None:
    pass