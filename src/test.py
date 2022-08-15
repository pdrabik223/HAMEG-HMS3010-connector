from datetime import datetime
from Requests import system
from device import connect, send_await_resp


if __name__ == "__main__":
    device = connect(0x0403, 0xED72)

    send_await_resp(device, system.Date.set(datetime(day=12, year=2013, month=1)))
    print(send_await_resp(device, system.Date.get()))

    while True:
        command = input("command: ")
        resp = send_await_resp(device, command)
        print(f"response: {resp[0]}")
        print(f"          {resp[1]}")
