import usb.core
import usb.util

class UsbDev:
    def __init__(self, VID, PID):
        self.output_ep = None
        self.input_ep = None
        self.VID = VID
        self.PID = PID
        self.device = usb.core.find(idVendor = VID, idProduct = PID)
        if self.device is None:
            raise AttributeError('Failed to connect')

    def check_device(self, dev_name=None):
        if dev_name is None:
            raise ValueError("device name provided is None")
        if self.device.product != dev_name:
            raise ValueError('Wrong type of product connected to host')

    def config_device(self):
        self.device.set_configuration()
        cfg = self.device.get_active_configuration()
        self.output_ep = usb.util.find_descriptor(cfg[(0, 0)], custom_match=lambda e:
            usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_OUT)
        self.input_ep = usb.util.find_descriptor(cfg[(0, 0)], custom_match=lambda e:
            usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_IN)

    def read_string(self):
        if self.input_ep is not None:
            ret_array = self.device.read(self.input_ep.bEndpointAddress,
                                      self.input_ep.wMaxPacketSize)
            self.device.clear_halt(self.input_ep)
            return ''.join([chr(x) for x in ret_array])  # always returns 1
        
    def send(self, payload :str)->None:
        self.device.write(self.input_ep.bEndpointAddress, payload)        
        
        
        
        
        

driver = UsbDev(0x0403, 0xed72)  
# driver.check_device('HAMEG HMS3010')
print(f"HAMEG device info:\n{driver.device}")
driver.config_device()
print(driver.input_ep.bEndpointAddress)
driver.send("*IDN?\n")    
print(driver.read_string())