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


class HTTPException(CallofDutyException):
    """Exception which is thrown when an HTTP request operation fails."""

    def __init__(self, res, data):
        self.res = res
        self.message: str = "An unknown error occurred"

        if isinstance(data, dict):
            try:
                data: dict = data.get("data")
                self.message: str = data.get("message", self.message)
            except AttributeError:
                self.message: str = str(data)

        super().__init__(f"HTTP {self.res.status_code} - {self.message}")


class Forbidden(HTTPException):
    """Exception which is thrown when HTTP status code 403 occurs."""

    pass


class NotFound(HTTPException):
    """Exception which is thrown when HTTP status code 404 occurs."""

    pass
