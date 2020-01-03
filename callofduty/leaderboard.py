import logging

from .enums import GameType, Platform, TimeFrame, Title
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
    gameMode : str, optional
        Game mode to get the leaderboard for (default is Career.)
    timeFrame : callofduty.TimeFrame, optional
        Time Frame to get the leaderboard for (default is All-Time.)
    page : int, optional
        Leaderboard page to get (default is 1.)
    """

    _type = "leaderboard"

    def __init__(self, client: object, data: dict):
        super().__init__(client)

        self.title = Title(data.pop("title"))
        self.platform = Platform(data.pop("platform"))
        self.gameType = GameType(data.pop("leaderboardType"))
        self.gameMode = data.pop("gameMode")
        self.timeFrame = TimeFrame(data.pop("timeFrame"))
        self.page = data.pop("page")

        self.pages = data.pop("totalPages")
        self.columns = data.pop("columns")
        self.entries = data.pop("entries")

    async def players(self):
        """
        Get the players from a Call of Duty leaderboard.

        Returns
        -------
        list
            Array containing Player objects for each Leaderboard entry.
        """

        return await self._client.GetLeaderboardPlayers(
            self.title,
            self.platform,
            gameType=self.gameType,
            gameMode=self.gameMode,
            timeFrame=self.timeFrame,
            page=self.page,
        )
