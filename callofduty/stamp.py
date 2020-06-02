import logging
from typing import Dict, List, Union

from .enums import Mode, Platform, Title
from .object import Object
from .player import Player

log: logging.Logger = logging.getLogger(__name__)


class AuthenticityStamp(Object):
    """
    Represents a Call of Duty Authenticity Stamp object.

    Parameters
    ----------
    platform : callofduty.Platform
        Platform of the player.
    username : str
        Player's username for the designated platform.
    title : callofduty.Title
        Title which the match took place.
    mode : callofduty.Mode
        Call of Duty mode which the match took place.
    players : list
        Array of Player objects for players present when the match ended.
    playersLeft : list
        Array of Player objects for players who left the match.
    data : dict
        JSON data for the requested Authenticity Stamp.
    settings : dict
        JSON data for the game settings of the requested Authenticity Stamp.
    stats : dict
        JSON data for the statistics of the player of the requested Authenticity Stamp.
    """

    _type: str = "AuthenticityStamp"

    def __init__(self, client, data: dict):
        super().__init__(client)

        self.platform: Platform = Platform(data.pop("platform"))
        self.username: str = data.pop("username")
        self.title: Title = Title(data.pop("title"))
        self.mode: Mode = Mode(data.pop("mode"))
        self.players: List[Player] = []
        self.playersLeft: List[Player] = []
        self.data: Dict[str, Union[int, str, bool, None]] = {}
        self.settings: Dict[str, Union[float, bool]] = data.pop("gameSettings")
        self.stats: Dict[str, Union[float]] = data.pop("playerStats")

        for _player in data.pop("partyMembers"):
            self.players.append(
                Player(self, {"platform": self.platform, "username": _player})
            )

        for _player in data.pop("partyMembersLeft"):
            self.players.append(
                Player(self, {"platform": self.platform, "username": _player})
            )

        for key in data:
            if (isinstance(data[key], dict) is False) and (
                isinstance(data[key], list) is False
            ):
                self.data[key] = data[key]
