from typing import Union


class CallofDutyException(Exception):
    """Base exception class for CallofDuty.py"""

    pass


class ClientException(CallofDutyException):
    """Exception which is thrown when an operation in the Client class fails."""

    pass


class LoginFailure(ClientException):
    """
    Exception which is thrown when authentication fails due to incorrect
    credentials or an unknown error.
    """

    pass


class InvalidPlatform(ClientException):
    """
    Exception which is thrown when an invalid platform is passed to any
    client function.
    """

    pass


class InvalidTitle(ClientException):
    """
    Exception which is thrown when an invalid title is passed to any
    client function.
    """

    pass


class InvalidMode(ClientException):
    """
    Exception which is thrown when an invalid mode is passed to any
    client function.
    """

    pass


class InvalidLanguage(ClientException):
    """
    Exception which is thrown when an invalid language is passed to any
    client function.
    """

    pass


class InvalidTimeFrame(ClientException):
    """
    Exception which is thrown when an invalid time frame is passed to any
    client function.
    """

    pass


class InvalidGameType(ClientException):
    """
    Exception which is thrown when an invalid game type is passed to any
    client function.
    """

    pass


class InvalidReaction(ClientException):
    """
    Exception which is thrown when an invalid reaction is passed to any
    client function.
    """

    pass


class HTTPException(CallofDutyException):
    """
    Exception which is thrown when an HTTP request operation fails.

    Parameters
    ----------
    statusCode : int
        HTTP status code of the request.
    res : dict
        Response of the HTTP request.
    """

    def __init__(self, statusCode: int, res: Union[dict, list, str]):
        if isinstance(res, dict):
            try:
                message: Union[dict, list, str] = res["data"].get("message", res)
            except AttributeError:
                # This allows us to capture reasoning from the Squads
                # endpoints which don't follow the usual response structure.
                message: Union[dict, list, str] = res.get("data", res)
            except KeyError:
                # This allows us to capture reasoning from the legacy
                # endpoints which don't follow the usual response structure.
                message: Union[dict, list, str] = res.get("message", res)
        else:
            message: Union[dict, list, str] = res

        super().__init__(f"HTTP {statusCode} - {message}")


class Forbidden(HTTPException):
    """Exception which is thrown when HTTP status code 403 occurs."""

    pass


class NotFound(HTTPException):
    """Exception which is thrown when HTTP status code 404 occurs."""

    pass
