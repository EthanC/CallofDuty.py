import logging

from .enums import GameMode, GameType, Language, Mode, Platform, TimeFrame, Title
from .leaderboard import Leaderboard
from .match import Match
from .player import Player
from .squad import Squad
from .utils import (
    VerifyGameMode,
    VerifyGameType,
    VerifyLanguage,
    VerifyMode,
    VerifyPlatform,
    VerifyTimeFrame,
    VerifyTitle,
)

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

    async def GetNewsFeed(self, language: Language = Language.English):
        """
        Get the Call of Duty franchise feed, includes blog posts and
        the Companion App message of the day.

        Parameters
        ----------
        language : callofduty.Language, optional
            Language to use for localization data (default is English.)

        Returns
        -------
        dict
            JSON data containing the Call of Duty franchise feed.
        """

        return await self.http.GetNewsFeed(language.value)

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

    async def GetMyIdentities(self):
        """
        Get the Title Identities for the authenticated Call of Duty player.

        Returns
        -------
        list
            Array of identities containing title, platform, username, and more.
        """

        data = (await self.http.GetMyIdentities())["data"]

        identities = []

        for identity in data["titleIdentities"]:
            identities.append(
                {
                    "title": Title(identity.pop("title")),
                    "platform": Platform(identity.pop("platform")),
                    "username": identity["username"],
                    "activeDate": identity["activeDate"],
                    "activityType": identity["activityType"],
                }
            )

        return identities

    async def GetMyAccounts(self):
        """
        Get the linked Accounts for the authenticated Call of Duty player.

        Returns
        -------
        list
            Array of Player objects for the linked accounts.
        """

        data = (await self.http.GetMyAccounts())["data"]

        accounts = []

        for account in data.keys():
            accounts.append(
                Player(
                    self, {"platform": account, "username": data[account]["username"]}
                )
            )

        return accounts

    async def GetMyFriends(self):
        """
        Get the Friends of the authenticated Call of Duty player.

        Returns
        -------
        list
            Array of Player objects for the friends.
        """

        data = (await self.http.GetMyFriends())["data"]

        friends = []

        for friend in data["uno"]:
            friends.append(
                Player(
                    self,
                    {
                        "platform": friend["platform"],
                        "username": friend["username"],
                        "accountId": friend.get("accountId"),
                        "online": friend["status"]["online"],
                    },
                )
            )

        for _platform in data["firstParty"]:
            for friend in data["firstParty"][_platform]:
                friends.append(
                    Player(
                        self,
                        {
                            "platform": friend["platform"],
                            "username": friend["username"],
                            "accountId": friend.get("accountId"),
                            "avatarUrls": [friend.get("avatarUrlLargeSsl")],
                            "online": friend["status"]["online"],
                        },
                    )
                )

                identities = friend.get("identities", [])

                for _platform in identities:
                    friends.append(
                        Player(
                            self,
                            {
                                "platform": friend["identities"][_platform]["platform"],
                                "username": friend["identities"][_platform]["username"],
                                "accountId": friend["identities"][_platform][
                                    "accountId"
                                ],
                                "avatarUrls": [
                                    friend["identities"][_platform].get(
                                        "avatarUrlLargeSsl"
                                    )
                                ],
                            },
                        )
                    )

        return friends

    async def GetMyFriendRequests(self):
        """
        Get the incoming and outgoing Friend Requests for the authenticated
        Call of Duty player.

        Returns
        -------
        dict
            JSON data of the player's friend requests.
        """

        data = (await self.http.GetMyFriends())["data"]

        incoming = []
        outgoing = []

        for request in data["incomingInvitations"]:
            incoming.append(
                Player(
                    self,
                    {
                        "platform": request["platform"],
                        "username": request["username"],
                        "accountId": request.get("accountId"),
                        "online": request["status"]["online"],
                    },
                )
            )

        for request in data["outgoingInvitations"]:
            outgoing.append(
                Player(
                    self,
                    {
                        "platform": request["platform"],
                        "username": request["username"],
                        "accountId": request.get("accountId"),
                        "online": request["status"]["online"],
                    },
                )
            )

        return {"incoming": incoming, "outgoing": outgoing}

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

    async def GetLeaderboard(self, title: Title, platform: Platform, **kwargs):
        """
        Get a Call of Duty leaderboard.

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
        timeFrame : callofduty.TimeFrame, optional
            Time Frame to get the leaderboard for (default is All-Time.)
        page : int, optional
            Leaderboard page to get (default is 1.)

        Returns
        -------
        object
            Leaderboard object representing the specified details.
        """

        gameType = kwargs.get("gameType", GameType.Core)
        gameMode = kwargs.get("gameMode", GameMode.Career)
        timeFrame = kwargs.get("timeFrame", TimeFrame.AllTime)
        page = kwargs.get("page", 1)

        VerifyTitle(title)
        VerifyPlatform(platform)
        VerifyGameType(gameType)
        VerifyGameMode(gameMode)
        VerifyTimeFrame(timeFrame)

        return Leaderboard(
            self,
            (
                await self.http.GetLeaderboard(
                    title.value,
                    platform.value,
                    gameType.value,
                    gameMode.value,
                    timeFrame.value,
                    page,
                )
            )["data"],
        )

    async def GetPlayerLeaderboard(
        self, title: Title, platform: Platform, username: str, **kwargs
    ):
        """
        Get a Call of Duty leaderboard.

        Parameters
        ----------
        title : callofduty.Title
            Call of Duty title which the leaderboard represents.
        platform : callofduty.Platform
            Platform to get which the leaderboard represents.
        username : str
            Player's username for the designated platform.
        gameType : callofduty.GameType, optional
            Game type to get the leaderboard for (default is Core.)
        gameMode : callofduty.GameMode, optional
            Game mode to get the leaderboard for (default is Career.)
        timeFrame : callofduty.TimeFrame, optional
            Time Frame to get the leaderboard for (default is All-Time.)

        Returns
        -------
        object
            Leaderboard object representing the specified details.
        """

        gameType = kwargs.get("gameType", GameType.Core)
        gameMode = kwargs.get("gameMode", GameMode.Career)
        timeFrame = kwargs.get("timeFrame", TimeFrame.AllTime)

        VerifyTitle(title)
        VerifyPlatform(platform)
        VerifyGameType(gameType)
        VerifyGameMode(gameMode)
        VerifyTimeFrame(timeFrame)

        return Leaderboard(
            self,
            (
                await self.http.GetPlayerLeaderboard(
                    title.value,
                    platform.value,
                    username,
                    gameType.value,
                    gameMode.value,
                    timeFrame.value,
                )
            )["data"],
        )

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
