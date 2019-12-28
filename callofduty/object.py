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

    _type = None

    def __init__(self, client: object):
        self._client = client

    @property
    def type(self):
        return self._type

    def __repr__(self):
        reprStr = self.__class__.__name__

        return f"<{reprStr}>"

    def __str__(self):
        return self.__repr__()
