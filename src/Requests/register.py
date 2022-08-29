import datetime
from pickletools import uint8
from typing import Any, Callable, List, Optional
from requests.base_request import Request
from requests.utils import parse_to_csv
from utils import get_or_raise, handle_response

REGISTER_HEADER = "*"


class CLS(Request):
    CLS_HEADER = "CLS"

    @staticmethod
    def send() -> "CLS":
        """
        Resets state and error list and deletes the OPC state

        Example:
            dev.send_await_resp(register.CLS.send())

        Returns:
            CLS: Setter for CLS command
        """
        return CLS()

    def __init__(self) -> None:
        super().__init__()
        self.mode = Request.Mode.SETTER

    def _send(self) -> str:
        return "".join([REGISTER_HEADER, self.CLS_HEADER])

    def _receive(self, response: str) -> Optional[uint8]:
        return handle_response(
            response=response, no_params=0, cast_func=None, mode=self.mode
        )


class ESE(Request):

    ESE_HEADER = "ESE"

    def __init__(self, new_seser_value: uint8 = None, mode=Request.Mode.GETTER) -> None:
        super().__init__()
        self.mode = mode
        self.new_seser_value = new_seser_value

    @staticmethod
    def send(new_seser_value: uint8) -> "ESE":
        """
        Reset error list and delete the OPC state

        Args:
            new_seser_value (uint8): new value for SES register

        Example:
            dev.send_await_resp(register.ESE.send(128))

        Returns:
            ESE: Setter for ESE command
        """
        new_seser_value = get_or_raise(new_seser_value, uint8, "new_seser_value")
        return ESE(new_seser_value, mode=Request.Mode.SETTER)

    @staticmethod
    def receive() -> "ESE":
        """
        Get current state of error list

        Example:
            dev.send_await_resp(register.ESE.receive())

        Returns:
            ESE: Getter for error list
        """
        return ESE(mode=Request.Mode.GETTER)

    def _send(self: "ESE") -> str:
        if self.mode == Request.Mode.GETTER:
            return ":".join([REGISTER_HEADER, self.ESE_HEADER]) + " ?"
        else:
            return (
                ":".join([REGISTER_HEADER, self.ESE_HEADER])
                + " "
                + str(self.new_seser_value)
            )

    def _receive(self, response: str) -> Optional[uint8]:
        return handle_response(
            response=response,
            no_params=1,
            cast_func=lambda param_list: uint8(param_list[0]),
        )
