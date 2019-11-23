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


class InvalidMatchId(ClientException):
    pass


class InvalidPlatform(ClientException):
    pass


class InvalidProfile(ClientException):
    pass


class UserNotFound(ClientException):
    pass


class InvalidTitle(ClientException):
    pass


class InvalidMode(ClientException):
    pass


class HTTPException(CallofDutyException):
    """Exception which is thrown when an HTTP request operation fails."""

    def __init__(self, res, data):
        self.res = res
        self.message = "An unknown error occurred"

        if isinstance(data, dict):
            data = data.get("data")
            self.message = data.get("message", self.message)

        super().__init__(f"{self.res.status} {self.res.reason} - {self.message}")


class Forbidden(HTTPException):
    """Exception which is thrown when HTTP status code 403 occurs."""

    pass


class NotFound(HTTPException):
    """Exception which is thrown when HTTP status code 404 occurs."""

    pass
