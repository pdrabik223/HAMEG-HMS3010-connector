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
    return (resp, decoded)


if __name__ == "__main__":
    device = connect(0x0403, 0xED72)

    while True:
        command = input("command: ")
        resp = send(device, command)
        print(f"response: {resp[0]}")
        print(f"          {resp[1]}")
