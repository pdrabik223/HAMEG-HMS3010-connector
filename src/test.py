from datetime import datetime
from Requests import system
from device import Device


if __name__ == "__main__":
    device = Device.connect_via_vip_pid(0x0403, 0xED72)

    device.send(system.Date.set(datetime(day=12, year=2013, month=1)))
    device.send_await_resp(system.Date.get())

    while True:
        command = input("command: ")
        resp = device.send_await_resp(command)
        print(f"response: {resp[0]}")
        print(f"          {resp[1]}")
