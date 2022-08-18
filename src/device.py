from copyreg import constructor
from time import sleep
from typing import Any
import usb.core
import usb.util
import logging

from Requests.request import Request
class Device:
    
    def __init__(self, device) -> None:
        self.device = device
        self.device.set_configuration()
        
    @staticmethod
    def connect_using_vid_pid(idVendor, idProduct):
        logging.debug(f"connecting do device with pid: {idProduct}, vid: {idVendor}")
        
        device = usb.core.find(idVendor=idVendor, idProduct=idProduct)
        if device is None:
            raise ValueError("Device is not found")

        logging.debug(f"connected do device with pid: {idProduct}, vid: {idVendor}")
        return Device(device)

    def _send_str(self, command: str):
        if not isinstance(command, str):
            raise TypeError(f"expected cmd to be str, received {type(command)}")

        if command is None or len(command) == 0:
            raise ValueError(f"cmd has to be not empty string, received: {command}")
        # commands send to device must end with terminal character
        if command[-1] != "\n":
            command += "\n"
        logging.debug(f"writing to device, message: {command}")
        try:
            self.device.write(0x2, command)
        except Exception:
            logging.error(f"error occurred while writing to device", exc_info=True)
            raise


    def send_await_resp(self, cmd: Any) -> Any:
        if isinstance(cmd, str):
            self._send_str(command=cmd)

        if isinstance(cmd, Request):
            self._send_str( command=cmd._send())
            if cmd.mode == Request.Mode.SETTER:
                return

        resp = self.device.read(0x81, 1_000_000, 10000)

        # Following lines are hack
        # problem seems to be that after sending message multiple readout are required to get response
        # the delay between readouts is not important, can be as short as 0.1 s
        # seems like a problem with buffer somewhere, following while statement waits for non-empty readout
        # thus avoiding the issue, this will come back tho
        # TODO find the source of this problem
        counter = 0
        while len(resp) == 2:
            sleep(0.2)
            resp = self.device.read(0x81, 1_000_000, 10000)
            counter += 1
            if counter > 5:
                break

        try:
            decoded = bytearray(resp).decode("utf-8")
        except Exception as ex:
            return (resp, f"fail with error message: {str(ex)}")

        if isinstance(cmd, str):
            return (resp, decoded)

        if isinstance(cmd, Request):
            return cmd._receive(decoded)
