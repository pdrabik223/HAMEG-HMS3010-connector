from enum import Enum
from typing import Any


class Request:
    class Mode(Enum):
        """
        some Request can act both as setters and as getters
        the System.Date depending on arguments presented can update date on device
        or retrieve current date from

        Args:
            Enum (_type_): _description_
        """

        SETTER = "setter"
        GETTER = "getter"

    mode: Mode = None

    def _send(self) -> str:
        pass

    def _receive(self, response: str) -> Any:
        pass
