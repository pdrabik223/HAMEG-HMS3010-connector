from time import sleep
import usb.core
import usb.util


def connect(vid, pid):
    dev = usb.core.find(idVendor=vid, idProduct=pid)
    if dev is None:
        raise ValueError("Device is not found")

    dev.set_configuration()
    return dev


cmd = "*ESE?\n"


def send(dev, cmd: str):
    if len(command) != 0:
        cmd += "\n"
        dev.write(0x2, cmd)
        sleep(0.5)
    resp = dev.read(0x81, 1_000_000, 1000)
    try:
        decoded = bytearray(resp).decode("utf-8")
    except Exception as ex:
        return (resp, f"fail with error message: {str(ex)}")
    return (resp, decoded)


if __name__ == "__main__":
    device = connect(0x0403, 0xED72)

    while True:
        command = input("command: ")
        resp = send(device, command)
        print(f"response: {resp[0]}")
        print(f"          {resp[1]}")
