import logging

from .enums import Platform, Title
from .errors import InvalidTitle

log = logging.getLogger(__name__)


class Squad:
    def __init__(self, http: object):
        self.http = http
