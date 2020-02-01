import logging
from typing import Optional

from .client import Client

log: logging.Logger = logging.getLogger(__name__)


class Object:
    """
    Represents a generic Call of Duty object.

    Parameters
    ----------
    client : callofduty.Client
        Client which manages communication with the Call of Duty API.
    """

    _type: Optional[str] = None

    def __init__(self, client: Client):
        self._client: Client = client

    @property
    def type(self) -> Optional[str]:
        return self._type

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"

    def __str__(self) -> str:
        return self.__repr__()
