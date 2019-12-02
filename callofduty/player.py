import logging

from .enums import Mode, Platform, Title
from .object import Object

log = logging.getLogger(__name__)


class Player(Object):
    """
    Represents a Call of Duty player object.

    Parameters
    ----------
    platform : callofduty.Platform
        Platform of the player.
    username : str
        Player's username for the designated platform.
    accountId : int, optional
        Account ID for the player's designated platform (typically Activision.)
    avatarUrls : list, optional
        Array of url strings which return an image of the player's avatar.
    """

    _type = "player"

    def __init__(self, client: object, data: dict):
        super().__init__(client, data)

        self.platform = Platform(data.pop("platform"))
        self.username = data.pop("username")
        self.accountId = data.pop("accountId", None)
        self.avatarUrls = data.pop("avatarUrls", [])

    async def profile(self, title: Title, mode: Mode):
        """
        Get the Call of Duty player's profile for the specified title and mode.

        Parameters
        ----------
        title : callofduty.Title
            Call of Duty title to get the player's profile from.
        mode: callofduty.Mode
            Call of Duty mode to get the player's profile from.

        Returns
        -------
        dict
            JSON data of the player's complete profile for the requested
            title and mode.
        """

        return await self._client.GetPlayerProfile(
            self.platform, self.username, title, mode
        )

    async def matches(self, title: Title, mode: Mode, **kwargs):
        """
        Get the Call of Duty player's match history for the specified title and mode.

        Parameters
        ----------
        title : callofduty.Title
            Call of Duty title to get the player's matches from.
        mode: callofduty.Mode
            Call of Duty mode to get the player's matches from.
        limit : int, optional
            Number of matches which will be returned.
        startTimestamp : int, optional
            Unix timestamp representing the earliest time which a returned
            match should've occured.
        endTimestamp : int, optional
            Unix timestamp representing the latest time which a returned
            match should've occured.

        Returns
        -------
        list
            Array of Match objects.
        """

        return await self._client.GetPlayerMatches(
            self.platform, self.username, title, mode, **kwargs
        )

    async def squad(self):
        """
        Get the Call of Duty player's Squad.

        Returns
        -------
        object
            Squad object for the requested Squad.
        """

        return await self._client.GetPlayerSquad(self.platform, self.username)
