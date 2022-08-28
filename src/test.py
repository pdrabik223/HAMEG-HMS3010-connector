from datetime import datetime
from requests import system
from device import Device


if __name__ == "__main__":
    dev = Device.connect_using_vid_pid(idVendor=0x0403, idProduct=0xED72)

    print("current date:")
    print(dev.send_await_resp(system.Date.receive()))

    print("set date to NOW!")
    dev.send_await_resp(system.Time.send(datetime.now()))

    print("current date:")
    print(dev.send_await_resp(system.Time.receive()))

    # while True:
    #     command = input("command: ")
    #     resp = dev.send_await_resp(command)
    #     print(f"response: {resp[0]}")
    #     print(f"          {resp[1]}")
