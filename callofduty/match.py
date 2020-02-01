import logging
from typing import List

from .enums import Platform, Title
from .object import Object
from .player import Player

log: logging.Logger = logging.getLogger(__name__)


class Match(Object):
    """
    Represents a Call of Duty match object.

    Parameters
    ----------
    id : int
        Match ID.
    platform : callofduty.Platform
        Platform of the player.
    title : callofduty.Title
        Title which the match took place.
    """

    _type: str = "Match"

    def __init__(self, client, data: dict):
        super().__init__(client)

        self.id: int = data.pop("id")
        self.platform: Platform = Platform(data.pop("platform"))
        self.title: Title = Title(data.pop("title"))

    async def teams(self) -> List[List[Player]]:
        """
        Get the teams which played in the match.

        Returns
        -------
        list
            Array containing two child arrays, one for each team. Each
            team's array contains Player objects which represent the
            players on the team.
        """

        return await self._client.GetMatchTeams(self.title, self.platform, self.id)

    async def details(self) -> dict:
        """
        Get the full details of the match.

        Returns
        -------
        dict
            JSON data containing the full details of the match.
        """

        return await self._client.GetMatchDetails(self.title, self.platform, self.id)
