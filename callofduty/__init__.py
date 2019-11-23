__title__ = "CallofDuty.py"
__author__ = "EthanC"
__version__ = "1.1.0"

import logging

from .auth import Auth, Login
from .client import Client
from .enums import *
from .errors import *
from .match import Match
from .user import User

try:
    from logging import NullHandler
except ImportError:

    class NullHandler(logging.Handler):
        def emit(self, record):
            pass


logging.getLogger(__name__).addHandler(NullHandler())
