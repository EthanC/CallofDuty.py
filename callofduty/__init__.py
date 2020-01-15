"""
CallofDuty.py is an asynchronous, object-oriented Python wrapper for
the Call of Duty API.

GitHub: https://github.com/EthanC/CallofDuty.py
"""

__title__: str = "CallofDuty.py"
__author__: str = "EthanC"
__version__: str = "0.1.0"

import logging

from .auth import Login
from .client import Client
from .enums import *
from .errors import *
from .leaderboard import Leaderboard
from .loot import LootItem, Season
from .match import Match
from .player import Player
from .squad import Squad

try:
    from logging import NullHandler
except ImportError:

    class NullHandler(logging.Handler):
        def emit(self, record):
            pass


logging.getLogger(__name__).addHandler(NullHandler())
