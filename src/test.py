from device import connect, send_await_resp
from quarries.system import AutoTune, Date


if __name__ == "__main__":
    device = connect(0x0403, 0xED72)

    print(send_await_resp(device, Date()))

    while True:
        command = input("command: ")
        resp = send_await_resp(device, command)
        print(f"response: {resp[0]}")
        print(f"          {resp[1]}")
