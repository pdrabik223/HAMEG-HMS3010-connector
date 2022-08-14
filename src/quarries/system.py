from enum import Enum
from statistics import mode
from typing import Any, Dict

SYSTEM = "SYSTEM"


class Request:
    class Mode(Enum):
        SETTER = "setter"
        GETTER = "getter"

    mode: Mode = None

    def _send(self) -> str:
        pass

    def _receive(self, response: str) -> Any:
        pass


class AutoTune(Request):

    AUTO_TUNE = "AUTOTUNE"
    mode = Request.Mode.GETTER

    def __init__(self) -> None:
        super().__init__()

    def _send(self) -> str:
        return ":".join([SYSTEM, self.AUTO_TUNE])

    def _receive(self, response: str) -> None:
        pass


class Date(Request):

    DATE = "DATE"

    def __init__(self, year: int = None, month: int = None, day: int = None) -> None:
        super().__init__()
        self.year = year
        self.month = month
        self.day = day
        if not (self.year and self.month and self.day):
            if self.year or self.month or self.day:
                raise ValueError("all parameters must be provided or none")
            else:
                self.mode = Request.Mode.GETTER
        else:
            self.mode = Request.Mode.SETTER

    def _send(self) -> str:
        if self.mode == Request.Mode.GETTER:
            return ":".join([SYSTEM, self.DATE]) + " ?"
        else:
            return ":".join([SYSTEM, self.DATE]) + " ".join(
                [self.year, self.month, self.day]
            )

    def _receive(self, response: str) -> Dict:
        if response[0:2] != '1`':
            raise ConnectionError("general response error")
        
        response = response[2:-1]
        
        if len(response) == 0:
            raise ConnectionError("general response error")
        
        response_parameters = response.split(",")

        response_dict = {"year": response_parameters[0], "month": response_parameters[1], "day": response_parameters[2]}
        return response_dict
