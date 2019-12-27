import logging

from .enums import GameMode, GameType, Platform, Title
from .object import Object

log = logging.getLogger(__name__)


class Leaderboard(Object):
    """
    Represents a Call of Duty leaderboard object.

    Parameters
    ----------
    title : callofduty.Title
        Call of Duty title which the leaderboard represents.
    platform : callofduty.Platform
        Platform to get which the leaderboard represents.
    gameType : callofduty.GameType, optional
        Game type to get the leaderboard for (default is Core.)
    gameMode : callofduty.GameMode, optional
        Game mode to get the leaderboard for (default is Career.)
    page : int, optional
        Leaderboard page to get (default is 1.)
    """

    _type = "leaderboard"

    def __init__(self, client: object, data: dict):
        super().__init__(client, data)

        self.title = Title(data.pop("title"))
        self.platform = Platform(data.pop("platform"))
        self.gameType = GameType(data.pop("leaderboardType"))
        self.gameMode = GameMode(data.pop("gameMode"))
        self.page = data.pop("page")

        self.requested = data.pop("resultsRequested")
        self.pages = data.pop("totalPages")
        self.columns = data.pop("columns")
        self.entries = data.pop("entries")
