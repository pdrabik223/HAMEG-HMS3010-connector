from copyreg import constructor
import datetime
from typing import Optional
from Requests.request import Request

SYSTEM = "SYSTEM"


class AutoTune(Request):
    """
    force Auto Tune on device, this action takes couple of seconds
    Setter mode:
        activate auto tune procedure on device
        
        example:
        ```
        dev.send_await_resp(system.AutoTune.send()) 
        ```
    """
    AUTO_TUNE = "AUTOTUNE"
    mode=Request.Mode.SETTER

    @staticmethod
    def send()->None:
        return AutoTune()

    def __init__(self) -> None:
        super().__init__()

    def _send(self) -> str:
        return ":".join([SYSTEM, self.AUTO_TUNE])

    def _receive(self, response: str) -> None:
        pass

class Date(Request):
    """
    Date control on device
    
    Setter mode:
        set specified date to device
        
        example:
        ```
        dev.send_await_resp(system.Date.send(datetime(year=2011,month=11,day=2))) 
        ```
        
    Getter mode:
        read current date from device
        
        example:
        ```
        print(dev.send_await_resp(system.Date.get()))
        ```
    """
    DATE = "DATE"
            
    @staticmethod
    def get():    
        return Date(mode=Request.Mode.GETTER)
    
    @staticmethod
    def send(new_date: datetime.date):
        if not isinstance(new_date, datetime.date):
            raise TypeError(f"new_date has incorrect type, expected datetime.date got {type(datetime.date)}")
        return Date(date=new_date, mode=Request.Mode.SETTER)
    
    
    def __init__(self, date: datetime.date = None, mode = Request.Mode.GETTER) -> None:
        super().__init__()
        self.mode = mode
        if mode == Request.Mode.SETTER:
            self.date: datetime.date = date

    def _send(self) -> str: 
        if self.mode == Request.Mode.GETTER:
            return ":".join([SYSTEM, self.DATE]) + " ?"
        else:
            return ":".join([SYSTEM, self.DATE]) + " " +  \
                   " ".join([str(self.date.year), str(self.date.month), str(self.date.day)])

    def _receive(self, response: str) -> Optional[datetime.date]:
        
        if response[0:2] != "1`":
            raise ConnectionError("general response error")
        response = response[2:-1]
        
        if self.mode == Request.Mode.GETTER:
        
            if len(response) == 0:
                raise ConnectionError("received empty response")

            response_parameters = response.split(",")

            return datetime.date(
                year=int(response_parameters[0]),
                month=int(response_parameters[1]),
                day=int(response_parameters[2]), )
        else:
            return None
