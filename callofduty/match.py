import logging

from .enums import Platform, Title
from .object import Object

log = logging.getLogger(__name__)


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

    _type = "match"

    def __init__(self, client: object, data: dict):
        super().__init__(client, data)

        self.id = data.pop("id")
        self.platform = Platform(data.pop("platform"))
        self.title = Title(data.pop("title"))

    async def teams(self):
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

    async def details(self):
        """
        Get the full details of the match.

        Returns
        -------
        dict
            JSON data containing the full details of the match.
        """

        return await self._client.GetMatchDetails(self.title, self.platform, self.id)
