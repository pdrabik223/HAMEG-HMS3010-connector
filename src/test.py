from datetime import datetime
from Requests import system
from device import Device


if __name__ == "__main__":
    dev = Device.connect_using_vid_pid(idVendor= 0x0403,idProduct= 0xED72)

    print(dev.send_await_resp(system.Date.receive()))
    print(dev.send_await_resp(system.Date.send(datetime(year=2011,month=11,day=2))))
    

    # while True:
    #     command = input("command: ")
    #     resp = dev.send_await_resp(command)
    #     print(f"response: {resp[0]}")
    #     print(f"          {resp[1]}")
