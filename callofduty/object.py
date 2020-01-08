import logging

log = logging.getLogger(__name__)


class Object:
    """
    Represents a generic Call of Duty object.

    Parameters
    ----------
    client : object
        Client which manages communication with the Call of Duty API.
    """

    _type: str = None

    def __init__(self, client: object):
        self._client: object = client

    @property
    def type(self) -> str:
        return self._type

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"

    def __str__(self) -> str:
        return self.__repr__()
