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


class UnexpectedResponseLineNumber(MarinerException):
    def __init__(self, response: str, expected: str) -> None:
        self.response = response
        self.expected = expected

    def get_title(self) -> str:
        return "Incorrect Response Line Number"

    def get_description(self) -> str:
        return (
            "The printer returned response for command "
            + f"{repr(self.response)} when Mariner3D "
            + "expected Line"
            + "Number {self.expected}"
        )
