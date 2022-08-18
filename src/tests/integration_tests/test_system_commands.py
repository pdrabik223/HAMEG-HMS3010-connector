import unittest

from datetime import datetime
from Requests import system
from device import Device


class TestDate(unittest.TestCase):
    def test_set_get(self):
        dev = Device.connect_using_vid_pid(idVendor= 0x0403,idProduct= 0xED72)
        dev.send_await_resp(system.Date.get(datetime(year=2011,month=11,day=2)))
        self.assertTrue(dev.send_await_resp(system.Date.get()) == datetime(year=2011,month=11,day=2))