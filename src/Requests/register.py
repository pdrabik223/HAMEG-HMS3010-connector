import datetime
from pickletools import uint8
from typing import Any, Callable, List, Optional
from Requests.base_request import Request
from Requests.utils import parse_to_csv
from utils import get_or_raise, handle_response

REGISTER_HEADING = "*"

class CLS(Request):
    """
    resets state and error list and deletes the OPC state
    
    Setter mode:
        reset error list and delete the OPC state
        
        example:
        ```
        dev.send_await_resp(system.CLS.send()) 
        ```
    """
    
    CLS_HEADING = "CLS"
    
    def __init__(self) -> None:
        super().__init__()
        self.mode=Request.Mode.SETTER
        
    @staticmethod
    def send():
        return CLS()
    
    def _send(self) -> str:
        return "".join([REGISTER_HEADING, self.CLS_HEADING])

class ESE(Request):
    """
    set or receive SESER (Standard Event State Enable Register) content as a decimal number
    
    Setter mode:
        reset error list and delete the OPC state
        
        example:
        ```
        dev.send_await_resp(system.ESE.send(128)) 
        ```
    Getter mode:
        reset error list and delete the OPC state
        
        example:
        ```
        dev.send_await_resp(system.ESE.receive()) 
        ```
    """
    
    ESE_HEADING = "ESE"
    
    def __init__(self, new_seser_value:uint8 = None, mode = Request.Mode.GETTER) -> None:
        super().__init__()
        self.mode = mode 
        self.new_seser_value = new_seser_value
    
    @staticmethod
    def send(new_seser_value:uint8):
        new_seser_value = get_or_raise(new_seser_value,uint8,"new_seser_value")
        return ESE(new_seser_value,mode=Request.Mode.SETTER)
    
    @staticmethod
    def receive()->uint8:
        return ESE(mode=Request.Mode.GETTER)
    
    
    def _send(self) -> str:
        if self.mode == Request.Mode.GETTER:
            return ":".join([REGISTER_HEADING, self.ESE_HEADING]) + " ?"
        else:
            return ":".join([REGISTER_HEADING, self.ESE_HEADING]) + " " + str(self.new_seser_value)
    
    def _receive(self, response: str) -> Optional[uint8]:
        return handle_response(response=response,no_params=1,cast_func=lambda param_list:uint8(param_list[0]))
        
