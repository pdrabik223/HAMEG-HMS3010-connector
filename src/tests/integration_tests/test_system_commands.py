import pytest

from datetime import datetime
from requests import system
from device import Device

class SystemCommands:
    def test_date_set_get(self):
        self.dev = Device.connect_using_vid_pid(idVendor=0x0403, idProduct=0xED72)
        self.dev.send_await_resp(system.Date.send(datetime(year=2011, month=11, day=2)))
        assert self.dev.send_await_resp(system.Date.receive()) == datetime(
            year=2011, month=11, day=2
        )

    def test_time_set_get(self):
        self.dev = Device.connect_using_vid_pid(idVendor=0x0403, idProduct=0xED72)
        self.dev.send_await_resp(
            system.Time.send(datetime(hour=21, minute=37, second=21))
        )
        assert self.dev.send_await_resp(system.Time.receive()) == datetime(
            hour=21, minute=37, second=21
        )
