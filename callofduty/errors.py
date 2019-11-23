class CallofDutyException(Exception):
    pass


class AuthenticationError(CallofDutyException):
    pass


class InvalidMatchIdError(CallofDutyException):
    pass

class InvalidPlatformError(CallofDutyException):
    pass

class InvalidProfileError(CallofDutyException):
    pass

class UserNotFoundError(CallofDutyException):
    pass