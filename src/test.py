from datetime import datetime
from requests import system
from device import Device


def console_ui():
    dev = Device.connect_using_vid_pid(idVendor=0x0403, idProduct=0xED72)
    while True:
        command = input("command: ")
        resp = dev.send_await_resp(command)
        print(f"response: {resp[0]}")
        print(f"          {resp[1]}")
def simple_ui():
    dev = Device.connect_using_vid_pid(idVendor=0x0403, idProduct=0xED72)


if __name__ == "__main__":
    console_ui()