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
    pages : int, optional
        Total number of pages available for the leaderboard.
    columns : list, optional
        Array of strings containing the column headers for the leaderboard.
    entries : list, optional
        Array of leaderboard entries.
    """

    _type: str = "leaderboard"

    def __init__(self, client: object, data: dict):
        super().__init__(client)

        self.title: Title = Title(data.pop("title"))
        self.platform: Platform = Platform(data.pop("platform"))
        self.gameType: GameType = GameType(data.pop("leaderboardType"))
        self.gameMode: str = data.pop("gameMode")
        self.timeFrame: TimeFrame = TimeFrame(data.pop("timeFrame"))
        self.page: int = data.pop("page")

        self.pages: int = data.pop("totalPages")
        self.columns: list = data.pop("columns")
        self.entries: list = data.pop("entries")

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
