import logging

from .enums import Language, Mode, Platform, Title
from .match import Match
from .player import Player
from .squad import Squad
from .utils import VerifyLanguage, VerifyMode, VerifyPlatform, VerifyTitle

log = logging.getLogger(__name__)


class Client:
    """Client which manages communication with the Call of Duty API."""

    def __init__(self, http: object):
        self.http = http

    async def Logout(self):
        """Close the client session."""

        await self.http.CloseSession()

    async def GetLocalize(self, language: Language = Language.English):
        """
        Get the localized strings used by the Call of Duty Companion App
        and website.

        Parameters
        ----------
        language : callofduty.Language, optional
            Language to use for localization data (default is English.)

        Returns
        -------
        dict
            JSON data containing localized strings.
        """

        VerifyLanguage(language)

        web = await self.http.GetWebLocalize(language.value)
        app = await self.http.GetAppLocalize(language.value)

        return {**web, **app}

    async def GetFriendFeed(self):
        """
        Get the Friend Feed of the authenticated Call of Duty player.

        Returns
        -------
        dict
            JSON data of the player's Friend Feed.
        """

        data = (await self.http.GetFriendFeed())["data"]

        players = []

        for i in data["identities"]:
            _player = Player(
                self, {"platform": i["platform"], "username": i["username"]}
            )
            players.append(_player)

        return {
            "events": data["events"],
            "players": players,
            "metadata": data["metadata"],
        }

    async def GetPlayer(self, platform: Platform, username: str):
        """
        Get a Call of Duty player using their platform and username.

        Parameters
        ----------
        platform : callofduty.Platform
            Platform to get the player from.
        username : str
            Player's username for the designated platform.

        Returns
        -------
        object
            Player object for the requested player.
        """

        VerifyPlatform(platform)

        return Player(self, {"platform": platform.value, "username": username})

    async def SearchPlayers(self, platform: Platform, username: str, **kwargs):
        """
        Search Call of Duty players by platform and username.

        Parameters
        ----------
        platform : callofduty.Platform
            Platform to get the players from.
        username : str
            Player's username for the designated platform.
        limit : int, optional
            Number of search results to return (default is no limit.)

        Returns
        -------
        list
            Array of Player objects matching the query.
        """

        VerifyPlatform(platform)

        data = (await self.http.SearchPlayer(platform.value, username))["data"]

        limit = kwargs.get("limit", 0)
        if limit > 0:
            data = data[:limit]

        results = []

        for player in data:
            accountId = player.get("accountId")
            if isinstance(accountId, str):
                # The API returns the accountId as a string
                accountId = int(accountId)

            avatarUrls = []
            if isinstance(player["avatar"], dict):
                for key in player["avatar"]:
                    avatarUrls.append(player["avatar"][key])

            data = {
                "platform": player["platform"],
                "username": player["username"],
                "accountId": accountId,
                "avatarUrls": avatarUrls,
            }

            results.append(Player(self, data))

        return results

    async def GetPlayerProfile(
        self, platform: Platform, username: str, title: Title, mode: Mode
    ):
        """
        Get a Call of Duty player's profile for the specified title and mode.

        Parameters
        ----------
        platform : callofduty.Platform
            Platform to get the player from.
        username : str
            Player's username for the designated platform.
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

        VerifyPlatform(platform)
        VerifyTitle(title)
        VerifyMode(mode)

        return (
            await self.http.GetPlayerProfile(
                platform.value, username, title.value, mode.value
            )
        )["data"]

    async def GetMatch(self, title: Title, platform: Platform, matchId: int):
        """
        Get a Call of Duty match using its title, platform, mode, and ID.

        Parameters
        ----------
        title : callofduty.Title
            Call of Duty title which the match occured on.
        platform : callofduty.Platform
            Platform to get the player from.
        matchId : int
            Match ID.

        Returns
        -------
        object
            Match object representing the specified details.
        """

        VerifyTitle(title)
        VerifyPlatform(platform)

        return Match(
            self, {"id": matchId, "platform": platform.value, "title": title.value,},
        )

    async def GetPlayerMatches(
        self, platform: Platform, username: str, title: Title, mode: Mode, **kwargs
    ):
        """
        Get a Call of Duty player's match history for the specified title and mode.

        Parameters
        ----------
        platform : callofduty.Platform
            Platform to get the player from.
        username : str
            Player's username for the designated platform.
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

        VerifyPlatform(platform)
        VerifyTitle(title)
        VerifyMode(mode)

        limit = kwargs.get("limit", 10)
        startTimestamp = kwargs.get("startTimestamp", 0)
        endTimestamp = kwargs.get("endTimestamp", 0)

        if platform == Platform.Activision:
            # The preferred matches endpoint does not currently support
            # the Activision (uno) platform.
            data = (
                await self.http.GetATVIPlayerMatches(
                    platform.value,
                    username,
                    title.value,
                    mode.value,
                    limit,
                    startTimestamp,
                    endTimestamp,
                )
            )["data"]["matches"]

            matches = []

            for _match in data:
                matches.append(
                    Match(
                        self,
                        {
                            # The API returns the matchId as a string
                            "id": int(_match["matchID"]),
                            "platform": platform.value,
                            "title": title.value,
                        },
                    )
                )
        else:
            data = (
                await self.http.GetPlayerMatches(
                    platform.value,
                    username,
                    title.value,
                    mode.value,
                    limit,
                    startTimestamp,
                    endTimestamp,
                )
            )["data"]

            matches = []

            for _match in data:
                matches.append(
                    Match(
                        self,
                        {
                            # The API returns the matchId as a string
                            "id": int(_match["matchId"]),
                            "platform": platform.value,
                            "title": title.value,
                        },
                    )
                )

        return matches

    async def GetMatchDetails(self, title: Title, platform: Platform, matchId: int):
        """
        Get a Call of Duty match's details.

        Parameters
        ----------
        title : callofduty.Title
            Call of Duty title which the match occured on.
        platform : callofduty.Platform
            Platform to get the match from.
        matchId : int
            Match ID.

        Returns
        -------
        dict
            JSON data containing the full details of the requested Call of Duty match.
        """

        VerifyPlatform(platform)
        VerifyTitle(title)

        return (await self.http.GetMatch(title.value, platform.value, matchId))["data"]

    async def GetMatchTeams(self, title: Title, platform: Platform, matchId: int):
        """
        Get the teams which played in a Call of Duty match.

        Parameters
        ----------
        title : callofduty.Title
            Call of Duty title which the match occured on.
        platform : callofduty.Platform
            Platform to get the match from.
        matchId : int
            Match ID.

        Returns
        -------
        list
            Array containing two child arrays, one for each team. Each
            team's array contains Player objects which represent the
            players on the team.
        """

        VerifyPlatform(platform)
        VerifyTitle(title)

        data = (await self.http.GetMatch(title.value, platform.value, matchId))["data"][
            "teams"
        ]

        # The API does not state which team is allies/axis, so no array
        # keys will be used.
        teams = []

        for team in data:
            # Current team iterator
            i = []

            for player in team:
                i.append(
                    Player(
                        self,
                        {
                            "platform": player["provider"],
                            "username": player["username"],
                            "accountId": player["unoId"],
                        },
                    )
                )

            teams.append(i)

        return teams

    async def GetSquad(self, name: str):
        """
        Get a Call of Duty Squad using its name.

        Parameters
        ----------
        name : str
            Name of Squad.

        Returns
        -------
        object
            Squad object for the requested Squad.
        """

        return Squad(self, (await self.http.GetSquad(name))["data"])

    async def GetPlayerSquad(self, platform: Platform, username: str):
        """
        Get a Call of Duty player's Squad using their platform and username.

        Parameters
        ----------
        platform : callofduty.Platform
            Platform to get the player from.
        username : str
            Player's username for the designated platform.

        Returns
        -------
        object
            Squad object for the requested Squad.
        """

        VerifyPlatform(platform)

        return Squad(
            self, (await self.http.GetPlayerSquad(platform.value, username))["data"]
        )

    async def GetMySquad(self):
        """
        Get the Squad of the authenticated Call of Duty player.

        Returns
        -------
        object
            Squad object for the requested Squad.
        """

        return Squad(self, (await self.http.GetMySquad())["data"])
