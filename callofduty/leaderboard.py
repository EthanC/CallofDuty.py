import logging
from typing import Dict, List, Union

from .enums import GameType, Platform, TimeFrame, Title
from .object import Object

log: logging.Logger = logging.getLogger(__name__)


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
        Array of Leaderboard Entry objects containing the entries for the leaderboard.
    """

    _type: str = "Leaderboard"

    def __init__(self, client, data: dict):
        super().__init__(client)

        self.title: Title = Title(data.pop("title"))
        self.platform: Platform = Platform(data.pop("platform"))
        self.gameType: GameType = GameType(data.pop("leaderboardType"))
        self.gameMode: str = data.pop("gameMode")
        self.timeFrame: TimeFrame = TimeFrame(data.pop("timeFrame"))
        self.page: int = data.pop("page")
        self.pages: int = data.pop("totalPages")
        self.columns: list = data.pop("columns")
        self.entries: List[LeaderboardEntry] = []

        for entry in data.pop("entries", []):
            # Leaderboard Entries don't include this value, so we'll just
            # add it manually.
            entry["platform"] = self.platform.value

            self.entries.append(LeaderboardEntry(self, entry))

    async def players(self) -> list:
        """
        Get the players from a Call of Duty leaderboard.

        Returns
        -------
        list
            Array of Player objects for each leaderboard entry.
        """

        return await self._client.GetLeaderboardPlayers(
            self.title,
            self.platform,
            gameType=self.gameType,
            gameMode=self.gameMode,
            timeFrame=self.timeFrame,
            page=self.page,
        )


class LeaderboardEntry(Object):
    """
    Represents a Call of Duty leaderboard entry object.

    Parameters
    ----------
    platform : callofduty.Platform
        Platform of the player.
    username : str
        Player's username for the designated platform.
    rank : int
        Leaderboard position for the designated entry.
    updated : int, optional
        Value in seconds representing how long ago the leaderboard entry was updated.
    rating : int, optional
        Unknown rating value.
    values : dict, optional
        JSON data containing values for the leaderboard entry.
    """

    _type: str = "LeaderboardEntry"

    def __init__(self, client, data: dict):
        super().__init__(client)

        self.platform: Platform = Platform(data.pop("platform"))
        self.username: str = data.pop("username")
        self.rank: int = int(data.pop("rank"))
        self.updated: int = int(data.pop("updateTime"))
        self.rating: int = data.pop("rating")
        self.values: Dict[str, Union[int, float]] = data.pop("values")
