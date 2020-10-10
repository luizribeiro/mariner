from abc import ABC, abstractmethod


class MarinerException(Exception, ABC):
    @abstractmethod
    def get_title(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_description(self) -> str:
        raise NotImplementedError


class UnexpectedPrinterResponse(MarinerException):
    def __init__(self, response: str) -> None:
        self.response = response

    def get_title(self) -> str:
        return "Unexpected Printer Response"

    def get_description(self) -> str:
        return f"The printer returned an unexpected response: {repr(self.response)}"
