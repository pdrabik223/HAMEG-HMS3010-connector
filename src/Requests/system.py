import datetime
from statistics import mode
from typing import Optional
from requests.base_request import Request
from requests.utils import handle_response, get_or_raise

SYSTEM_HEADER = "SYSTEM"


class AutoTune(Request):
    COMMAND = "AUTOTUNE"
    mode = Request.Mode.SETTER

    @staticmethod
    def send() -> None:
        """
        Request Auto Tune on device, this action takes couple of seconds

        Example:
            dev.send_await_resp(system.AutoTune.send())

        Returns:
            _type_: _description_
        """
        return AutoTune()

    def __init__(self) -> None:
        super().__init__()

    def _send(self) -> str:
        return ":".join([SYSTEM_HEADER, self.COMMAND])

    def _receive(self, response: str) -> Optional[datetime.date]:
        return handle_response(response, 0, None, self.mode)


class Date(Request):
    # Date control on device

    COMMAND = "DATE"

    def __init__(self, date: datetime.date = None, mode=Request.Mode.GETTER) -> None:
        super().__init__()
        self.mode = mode
        self.date = date

    @staticmethod
    def receive():
        """
        Read current date from device in datetime.date format

        Example:
            print(dev.send_await_resp(system.Date.receive()))

        Returns
            Date: getter object for date
        """
        return Date(mode=Request.Mode.GETTER)

    @staticmethod
    def send(new_date: datetime.date):
        """
        set specified date to device

        Args:
            new_date (datetime.date): new date

        Example:
            dev.send_await_resp(system.Date.send(datetime(year=2011,month=11,day=2)))
            
        Returns:
            Date: setter object for date
        """
        new_date = get_or_raise(new_date, datetime.date, "new_date")
        return Date(date=new_date, mode=Request.Mode.SETTER)

    def _send(self) -> str:
        if self.mode == Request.Mode.GETTER:
            return ":".join([SYSTEM_HEADER, self.COMMAND]) + " ?\n"
        else:
            return (
                ":".join([SYSTEM_HEADER, self.COMMAND])
                + " "
                + " ".join(
                    [str(self.date.year), str(self.date.month), str(self.date.day)]
                )
                +"\n"
            )

    def _receive(self, response: str) -> Optional[datetime.date]:

        return handle_response(
            response,
            3,
            cast_func=lambda param_list: datetime.date(
                year    =int(chr(param_list[0])),
                month   =int(chr(param_list[1])),
                day     =int(chr(param_list[2])),
            ),
            mode=self.mode,
        )


class Time(Request):
    #    Time control on device

    COMMAND = "TIME"

    def __init__(self, time: datetime.time = None, mode=Request.Mode.GETTER) -> None:
        super().__init__()
        self.mode = mode
        self.time = time

    @staticmethod
    def receive():
        """
        Read current time from device in datetime.time format

        Example:
            print(dev.send_await_resp(system.Time.receive()))

        Returns
            Time: getter object for time
        """
        return Time(mode=Request.Mode.GETTER)

    @staticmethod
    def send(new_time: datetime.time):
        """
        set specified date to device

        Args:
            new_date (datetime.time): new time

        Example:
            dev.send_await_resp(system.Time.send(datetime(hour=16,minute=12,second=10)))

        Returns:
            Time: setter object for time
        """
        new_time = get_or_raise(new_time, datetime.datetime, "new_time")
        return Time(time=new_time, mode=Request.Mode.SETTER)

    def _send(self) -> str:
        if self.mode == Request.Mode.GETTER:
            return ":".join([SYSTEM_HEADER, self.COMMAND]) + " ?"
        else:
            return (
                ":".join([SYSTEM_HEADER, self.COMMAND])
                + " "
                + " ".join(
                    [str(self.time.hour), str(self.time.minute), str(self.time.second)]
                )
            )

    def _receive(self, response: str) -> Optional[datetime.time]:

        return handle_response(
            response,
            3,
            cast_func  = lambda param_list: datetime.time(
                hour   = int(param_list[0]),
                minute = int(param_list[1]),
                second = int(param_list[2]),
            ),
            mode=self.mode,
        )
