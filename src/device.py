from time import sleep
from typing import Any
import usb.core
import usb.util
import logging

from quarries.system import Request


def connect(vid, pid):
    logging.debug(f"connecting do device with pid: {pid}, vid: {vid}")
    dev = usb.core.find(idVendor=vid, idProduct=pid)
    if dev is None:
        logging.error("Device is not found")
        raise ValueError("Device is not found")

    dev.set_configuration()
    logging.debug(f"connected do device with pid: {pid}, vid: {vid}")
    return dev


def _send_str(device, command: str):
    if not isinstance(command, str):
        logging.error(f"expected cmd to be str, received {type(command)}")
        raise TypeError(f"expected cmd to be str, received {type(command)}")

    if command is None or len(command) == 0:
        logging.error(f"cmd has to be not empty string, received: {command}")
        raise ValueError(f"cmd has to be not empty string, received: {command}")
    # commands send to device must end with terminal character
    if command[-1] != "\n":
        command += "\n"
    logging.debug(f"writing to device, message: {command}")
    try:
        device.write(0x2, command)
    except Exception as ex:
        logging.error(f"error accured while writing to device", exc_info=True)
        raise


def send_await_resp(dev, cmd: Any)->Any:
    if isinstance(cmd, str):
        _send_str(device=dev, command=cmd)
    if isinstance(cmd, Request):
        _send_str(device=dev, command=cmd._send())

    resp = dev.read(0x81, 1_000_000, 10000)

    # Following lines are hack
    # problem seems to be that after sending message multiple readout are required to get response
    # the delay between readouts is not important, can be as short as 0.1 s
    # seems like a problem with buffer somewhere, following while statement waits for non-empty readout
    # thus avoiding the issue, this will come back tho
    # TODO find the source of this problem
    counter = 0
    while len(resp) == 2:
        sleep(0.1)
        resp = dev.read(0x81, 1_000_000, 10000)
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
