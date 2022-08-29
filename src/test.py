from datetime import datetime
from requests import system
from device import Device


if __name__ == "__main__":
    dev = Device.connect_using_vid_pid(idVendor=0x0403, idProduct=0xED72)

    print(f"current date: {system.Date.receive()._send()}")
    print(dev.send_await_resp(system.Date.receive()))

    print(f"set date to NOW!: {system.Date.send(datetime.now())._send()}")
    dev.send_await_resp(system.Date.send(datetime.now()))

    print(f"current date:") #{system.Date.receive()._send()}
    # print(f"resp: {dev.send_await_resp(system.Date.receive()._send())}")
    print(dev.send_await_resp(system.Date.receive()))

    # while True:
    #     command = input("command: ")
    #     resp = dev.send_await_resp(command)
    #     print(f"response: {resp[0]}")
    #     print(f"          {resp[1]}")
