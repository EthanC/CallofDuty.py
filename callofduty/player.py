import logging
from typing import List, Optional

from .enums import Mode, Platform, Title
from .errors import InvalidPlatform
from .loadout import Loadout, LoadoutItem
from .object import Object

log: logging.Logger = logging.getLogger(__name__)


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
        Account ID for the player's designated platform (default is None.)
    avatarUrl : str, optional
        Url which returns an image of the player's avatar (default is None.)
    online : bool, optional
        Boolean indicating whether or not the player is currently online (default is False.)
    identities : list, optional
        Array of Player objects containing the player's identities (default is an empty list.)
    """

    _type: str = "Player"

    def __init__(self, client, data: dict):
        super().__init__(client)

        self.platform: Platform = Platform(data.pop("platform"))
        self.username: str = data.pop("username")
        self.accountId: Optional[int] = data.pop("accountId", None)
        self.avatarUrl: Optional[str] = data.pop("avatarUrl", None)
        self.online: bool = data.pop("online", False)
        self.identities: List[Player] = data.pop("identities", [])

    async def profile(self, title: Title, mode: Mode) -> dict:
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

    async def matches(self, title: Title, mode: Mode, **kwargs) -> list:
        """
        Get the Call of Duty player's match history for the specified title and mode.

        Parameters
        ----------
        title : callofduty.Title
            Call of Duty title to get the player's matches from.
        mode: callofduty.Mode
            Call of Duty mode to get the player's matches from.
        limit : int, optional
            Number of matches which will be returned (default is 10.)
        startTimestamp : int, optional
            Unix timestamp representing the earliest time which a returned
            match should've occured (default is None.)
        endTimestamp : int, optional
            Unix timestamp representing the latest time which a returned
            match should've occured (default is None.)

        Returns
        -------
        list
            Array of Match objects.
        """

        return await self._client.GetPlayerMatches(
            self.platform, self.username, title, mode, **kwargs
        )

    async def matchesSummary(self, title: Title, mode: Mode, **kwargs) -> dict:
        """
        Get the Call of Duty player's match history for the specified title and mode.

        Parameters
        ----------
        title : callofduty.Title
            Call of Duty title to get the player's matches from.
        mode: callofduty.Mode
            Call of Duty mode to get the player's matches from.
        limit : int, optional
            Number of matches which will be returned (default is 10.)
        startTimestamp : int, optional
            Unix timestamp representing the earliest time which a returned
            match should've occured (default is None.)
        endTimestamp : int, optional
            Unix timestamp representing the latest time which a returned
            match should've occured (default is None.)

        Returns
        -------
        dict
            JSON data containing recent matches summary.
        """

        return await self._client.GetPlayerMatchesSummary(
            self.platform, self.username, title, mode, **kwargs
        )

    async def leaderboard(self, title: Title, **kwargs):
        """
        Get the specified Leaderboard page which contains the Call of Duty player.

        Parameters
        ----------
        title : callofduty.Title
            Call of Duty title which the leaderboard represents.
        gameType : callofduty.GameType, optional
            Game type to get the leaderboard for (default is Core.)
        gameMode : str, optional
            Game mode to get the leaderboard for (default is Career.)
        timeFrame : callofduty.TimeFrame, optional
            Time Frame to get the leaderboard for (default is All-Time.)

        Returns
        -------
        object
            Leaderboard object representing the specified details.
        """

        return await self._client.GetPlayerLeaderboard(
            title, self.platform, self.username, **kwargs
        )

    async def loadouts(self, title: Title, **kwargs) -> List[Loadout]:
        """
        Get the Call of Duty player's loadouts for the specified title and mode.

        Parameters
        ----------
        title : callofduty.Title
            Call of Duty title to get the player's loadouts from.
        mode: callofduty.Mode, optional
            Call of Duty mode to get the player's loadouts from (default is Multiplayer.)

        Returns
        -------
        list
            Array of loadout objects.
        """

        return await self._client.GetPlayerLoadouts(
            self.platform, self.username, title, **kwargs
        )

    async def loadoutUnlocks(self, title: Title, **kwargs) -> List[LoadoutItem]:
        """
        Get the Call of Duty player's loadout unlocks for the specified title and mode.

        Parameters
        ----------
        title : callofduty.Title
            Call of Duty title to get the player's loadout unlocks from.
        mode: callofduty.Mode, optional
            Call of Duty mode to get the player's loadout unlocks from (default is Multiplayer.)

        Returns
        -------
        list
            Array of loadout item objects.
        """

        return await self._client.GetPlayerLoadoutUnlocks(
            self.platform, self.username, title, **kwargs
        )

    async def authenticityStamp(self, phrase: str, **kwargs):
        """
        Get the Call of Duty player's Authenticity Stamp for the specified phrase.

        Parameters
        ----------
        phrase : str
            Authenticity Stamp code.
        title : callofduty.Title, optional
            Call of Duty title to get the Authenticity Stamp from (default is Black Ops 4.)

        Returns
        -------
        callofduty.AuthenticityStamp
            AuthenticityStamp object representing the requested Authenticity Stamp.
        """

        return await self._client.GetAuthenticityStamp(
            self.platform, self.username, phrase, **kwargs
        )

    async def addFriend(self) -> str:
        """
        Send a Friend Request to the player's Activision ID.

        Returns
        -------
        str
            Status of the Friend Request.
        """

        if self.platform is not Platform.Activision:
            raise InvalidPlatform()

        return await self._client.AddFriend(self.accountId)

    async def removeFriend(self) -> str:
        """
        Remove a Friend or Friend Request to the player's Activision ID.

        Returns
        -------
        str
            Status of the Friend Request removal.
        """

        if self.platform is not Platform.Activision:
            raise InvalidPlatform()

        return await self._client.RemoveFriend(self.accountId)

    async def addFavorite(self) -> list:
        """
        Set the Player as a Favorite Friend.

        Returns
        -------
        list
            Array of Player objects of all Favorite Friends.
        """

        return await self._client.AddFavorite(self.platform, self.username)

    async def removeFavorite(self) -> list:
        """
        Remove the Player as a Favorite Friend.

        Returns
        -------
        list
            Array of Player objects of all Favorite Friends.
        """

        return await self._client.RemoveFavorite(self.platform, self.username)

    async def block(self) -> None:
        """
        Block communications to and from the specified Activision ID.

        Returns
        -------
        None
        """

        if self.platform is not Platform.Activision:
            raise InvalidPlatform()

        await self._client.BlockPlayer(self.accountId)

    async def unblock(self) -> None:
        """
        Unblock communications to and from the specified Activision ID.

        Returns
        -------
        None
        """

        if self.platform is not Platform.Activision:
            raise InvalidPlatform()

        await self._client.UnblockPlayer(self.accountId)

    async def squad(self):
        """
        Get the Call of Duty player's Squad.

        Returns
        -------
        object
            Squad object for the requested Squad.
        """

        return await self._client.GetPlayerSquad(self.platform, self.username)
