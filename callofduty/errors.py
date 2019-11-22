class CallofDutyException(Exception):
    pass


class AuthenticationError(CallofDutyException):
    pass


class InvalidMatchIdError(CallofDutyException):
    pass
