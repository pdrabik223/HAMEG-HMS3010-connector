from typing import Any, List, Callable, Optional

from requests.base_request import Request


def get_or_raise(
    variable: Any,
    cast_to_type: type,
    variable_name: str = "variable",
    can_be_none: bool = False,
) -> Any:

    if variable is None and not can_be_none:
        raise ValueError(f"{variable_name} can not be none")

    if variable is None and can_be_none:
        return variable

    if isinstance(variable, cast_to_type):
        return variable

    try:
        variable = cast_to_type(variable)
    except ValueError:
        raise TypeError(
            f"{variable_name} casting to {cast_to_type} failed, {type(variable)} can not be trivially converted to {cast_to_type}"
        )
    return variable


def parse_to_csv(message: str) -> List[str]:
    message = get_or_raise(message, str, "message")

    if len(message) == 0:
        raise ValueError("message can not be empty")

    return message.split(",")


def handle_response(
    response: str, no_params: int, cast_func: Callable, mode
) -> Optional[Any]:
    response = get_or_raise(response, str, "response")
    no_params = get_or_raise(no_params, int, "no_params")
    cast_func = get_or_raise(cast_func, Callable, "cast_func", True)
    mode = get_or_raise(mode, Request.Mode, "mode")



    if response[0] == "1":
        response = response[1:]
        if response[0] == "`":
            response = response[1:]
    else:
        raise Exception(f"General response error, received response: {response}")

    if mode == Request.Mode.GETTER:

        if r"\\n" in response:
            response.replace(r"\\n","")
        
        response = parse_to_csv(response)
        
        try:
            if len(response) != no_params:
                raise

            return cast_func(response)

        except Exception as ex:
            raise Exception(f"The response does not contain valid date, resp: {response}", ex)
    else:
        return None
