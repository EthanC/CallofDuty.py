import logging
from typing import List, Union

from .enums import GameType, Language, Mode, Platform, TimeFrame, Title
from .leaderboard import Leaderboard
from .loadout import Loadout, LoadoutItem
from .loot import Season
from .match import Match
from .player import Player
from .squad import Squad
from .utils import (
    StripHTML,
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

    def __init__(self, http):
        self.http = http

    async def GetLocalize(self, language: Language = Language.English) -> dict:
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

        web: dict = await self.http.GetWebLocalize(language.value)
        app: dict = await self.http.GetAppLocalize(language.value)

        return {**web, **app}

    async def GetNewsFeed(self, language: Language = Language.English) -> dict:
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

    async def GetFriendFeed(self, **kwargs) -> dict:
        """
        Get the Friend Feed of the authenticated Call of Duty player.

        Parameters
        ----------
        stripHTML : bool, optional
            Whether to strip the HTML formatting from rendered event strings (default is True.)

        Returns
        -------
        dict
            JSON data of the authenticated player's Friend Feed.
        """

        stripHTML: bool = kwargs.get("stripHTML", True)

        data: dict = (await self.http.GetFriendFeed())["data"]

        players: List[Player] = []
        for i in data["identities"]:
            _player: Player = Player(
                self, {"platform": i["platform"], "username": i["username"]}
            )
            players.append(_player)

        if stripHTML is True:
            for i in data["events"]:
                i["rendered"] = StripHTML(i["rendered"])

        return {
            "events": data["events"],
            "players": players,
            "metadata": data["metadata"],
        }

    async def GetMyIdentities(self) -> list:
        """
        Get the Title Identities for the authenticated Call of Duty player.

        Returns
        -------
        list
            Array of identities containing title, platform, username, and more.
        """

        data: dict = (await self.http.GetMyIdentities())["data"]

        identities: list = []

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

    async def GetMyAccounts(self) -> List[Player]:
        """
        Get the linked Accounts for the authenticated Call of Duty player.

        Returns
        -------
        list
            Array of Player objects for the linked accounts.
        """

        data: dict = (await self.http.GetMyAccounts())["data"]

        accounts: List[Player] = []

        for account in data.keys():
            accounts.append(
                Player(
                    self, {"platform": account, "username": data[account]["username"]}
                )
            )

        return accounts

    async def GetMyFriends(self) -> List[Player]:
        """
        Get the Friends of the authenticated Call of Duty player.

        Returns
        -------
        list
            Array of Player objects for the friends.
        """

        data: dict = (await self.http.GetMyFriends())["data"]

        friends: List[Player] = []

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
                i: list = friend.get("identities", [])
                identities: List[Player] = []

                for _platform in i:
                    identities.append(
                        Player(
                            self,
                            {
                                "platform": friend["identities"][_platform]["platform"],
                                "username": friend["identities"][_platform].get(
                                    "username"
                                ),
                                "accountId": friend["identities"][_platform][
                                    "accountId"
                                ],
                                "avatarUrl": friend["identities"][_platform].get(
                                    "avatarUrlLargeSsl"
                                ),
                            },
                        )
                    )

                friends.append(
                    Player(
                        self,
                        {
                            "platform": friend["platform"],
                            "username": friend["username"],
                            "accountId": friend.get("accountId"),
                            "avatarUrl": friend.get("avatarUrlLargeSsl"),
                            "online": friend["status"]["online"],
                            "identities": identities,
                        },
                    )
                )

        return friends

    async def GetMyFriendRequests(self) -> dict:
        """
        Get the incoming and outgoing Friend Requests for the authenticated
        Call of Duty player.

        Returns
        -------
        dict
            JSON data of the player's friend requests.
        """

        data: dict = (await self.http.GetMyFriends())["data"]

        incoming: List[Player] = []
        outgoing: List[Player] = []

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

    async def GetPlayer(self, platform: Platform, username: str) -> Player:
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

    async def SearchPlayers(
        self, platform: Platform, username: str, **kwargs
    ) -> List[Player]:
        """
        Search Call of Duty players by platform and username.

        Parameters
        ----------
        platform : callofduty.Platform
            Platform to get the players from.
        username : str
            Player's username for the designated platform.
        limit : int, optional
            Number of search results to return (default is None.)

        Returns
        -------
        list
            Array of Player objects matching the query.
        """

        VerifyPlatform(platform)

        data: dict = (await self.http.SearchPlayer(platform.value, username))["data"]

        limit: int = kwargs.get("limit", 0)
        if limit > 0:
            data = data[:limit]

        results: List[Player] = []

        for player in data:
            # The API returns the accountId as a string
            accountId: int = int(player.get("accountId"))

            avatar: Union[dict, str] = player.get("avatar")
            if isinstance(avatar, dict):
                avatar: Union[dict, str] = avatar["avatarUrlLargeSsl"]

            data = {
                "platform": player["platform"],
                "username": player["username"],
                "accountId": accountId,
                "avatarUrl": avatar,
            }

            results.append(Player(self, data))

        return results

    async def GetPlayerProfile(
        self, platform: Platform, username: str, title: Title, mode: Mode
    ) -> dict:
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
        VerifyMode(mode, title)

        return (
            await self.http.GetPlayerProfile(
                platform.value, username, title.value, mode.value
            )
        )["data"]

    async def GetMatch(self, title: Title, platform: Platform, matchId: int) -> Match:
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
    ) -> List[Match]:
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

        VerifyPlatform(platform)
        VerifyTitle(title)
        VerifyMode(mode, title)

        limit: int = kwargs.get("limit", 10)
        startTimestamp: int = kwargs.get("startTimestamp", 0)
        endTimestamp: int = kwargs.get("endTimestamp", 0)

        if platform == Platform.Activision:
            # The preferred matches endpoint does not currently support
            # the Activision (uno) platform.
            data: dict = (
                await self.http.GetPlayerMatchesDetailed(
                    platform.value,
                    username,
                    title.value,
                    mode.value,
                    limit,
                    startTimestamp,
                    endTimestamp,
                )
            )["data"]["matches"]

            matches: List[Match] = []

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
            data: dict = (
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

            matches: List[Match] = []

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

    async def GetPlayerMatchesSummary(
        self, platform: Platform, username: str, title: Title, mode: Mode, **kwargs
    ) -> dict:
        """
        Get a Call of Duty player's match history summary for the specified title and mode.

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

        VerifyPlatform(platform)
        VerifyTitle(title)
        VerifyMode(mode, title)

        limit: int = kwargs.get("limit", 10)
        startTimestamp: int = kwargs.get("startTimestamp", 0)
        endTimestamp: int = kwargs.get("endTimestamp", 0)

        return (
            await self.http.GetPlayerMatchesDetailed(
                platform.value,
                username,
                title.value,
                mode.value,
                limit,
                startTimestamp,
                endTimestamp,
            )
        )["data"]["summary"]

    async def GetMatchDetails(
        self, title: Title, platform: Platform, matchId: int
    ) -> dict:
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

    async def GetMatchTeams(
        self, title: Title, platform: Platform, matchId: int
    ) -> list:
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

        data: dict = (await self.http.GetMatch(title.value, platform.value, matchId))[
            "data"
        ]["teams"]

        # The API does not state which team is allies/axis, so no array
        # keys will be used.
        teams: list = []

        for team in data:
            # Current team iterator
            i: List[Player] = []

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

    async def GetLeaderboard(
        self, title: Title, platform: Platform, **kwargs
    ) -> Leaderboard:
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
        gameMode : str, optional
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

        gameType: GameType = kwargs.get("gameType", GameType.Core)
        gameMode: str = kwargs.get("gameMode", "career")
        timeFrame: TimeFrame = kwargs.get("timeFrame", TimeFrame.AllTime)
        page: int = kwargs.get("page", 1)

        VerifyTitle(title)
        VerifyPlatform(platform)
        VerifyGameType(gameType)
        VerifyTimeFrame(timeFrame)

        data: dict = (
            await self.http.GetLeaderboard(
                title.value,
                platform.value,
                gameType.value,
                gameMode,
                timeFrame.value,
                page,
            )
        )["data"]

        # Leaderboard responses don't include the timeFrame, so we'll
        # just add it manually.
        data["timeFrame"] = timeFrame.value

        return Leaderboard(self, data)

    async def GetPlayerLeaderboard(
        self, title: Title, platform: Platform, username: str, **kwargs
    ) -> Leaderboard:
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
        gameMode : str, optional
            Game mode to get the leaderboard for (default is Career.)
        timeFrame : callofduty.TimeFrame, optional
            Time Frame to get the leaderboard for (default is All-Time.)

        Returns
        -------
        object
            Leaderboard object representing the specified details.
        """

        gameType: GameType = kwargs.get("gameType", GameType.Core)
        gameMode: str = kwargs.get("gameMode", "career")
        timeFrame: TimeFrame = kwargs.get("timeFrame", TimeFrame.AllTime)

        VerifyTitle(title)
        VerifyPlatform(platform)
        VerifyGameType(gameType)
        VerifyTimeFrame(timeFrame)

        data: dict = (
            await self.http.GetPlayerLeaderboard(
                title.value,
                platform.value,
                username,
                gameType.value,
                gameMode,
                timeFrame.value,
            )
        )["data"]

        # Leaderboard responses don't include the timeFrame, so we'll
        # just add it manually.
        data["timeFrame"] = timeFrame.value

        return Leaderboard(self, data)

    async def GetLeaderboardPlayers(
        self, title: Title, platform: Platform, **kwargs
    ) -> List[Player]:
        """
        Get the players from a Call of Duty leaderboard.

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

        Returns
        -------
        list
            Array containing Player objects for each Leaderboard entry.
        """

        gameType: GameType = kwargs.get("gameType", GameType.Core)
        gameMode: str = kwargs.get("gameMode", "career")
        timeFrame: TimeFrame = kwargs.get("timeFrame", TimeFrame.AllTime)
        page: int = kwargs.get("page", 1)

        VerifyTitle(title)
        VerifyPlatform(platform)
        VerifyGameType(gameType)
        VerifyTimeFrame(timeFrame)

        data: dict = (
            await self.http.GetLeaderboard(
                title.value,
                platform.value,
                gameType.value,
                gameMode,
                timeFrame.value,
                page,
            )
        )["data"]

        # Leaderboard responses don't include the timeFrame, so we'll
        # just add it manually.
        data["timeFrame"] = timeFrame.value

        players: List[Player] = []
        for entry in Leaderboard(self, data).entries:
            players.append(
                Player(self, {"platform": platform.value, "username": entry.username})
            )

        return players

    async def GetAvailableMaps(
        self,
        title: Title,
        platform: Platform = Platform.PlayStation,
        mode: Mode = Mode.Multiplayer,
    ) -> list:
        """
        Get the Maps available in the specified Title for Heat Map use.

        Parameters
        ----------
        title : callofduty.Title
            Call of Duty title which the maps originate.
        platform : callofduty.Platform, optional
            Platform which the maps are available on (default is PlayStation.)
        mode: callofduty.Mode, optional
            Call of Duty mode to get the maps from (default is Multiplayer.)

        Returns
        -------
        list
            Array of Maps and the Game Modes which are available each map.
        """

        return (
            await self.http.GetAvailableMaps(title.value, platform.value, mode.value)
        )["data"]

    async def GetLootSeason(self, title: Title, season: int, **kwargs) -> Season:
        """
        Get a Call of Duty Loot Season by its title and number.

        Parameters
        ----------
        title : callofduty.Title
            Call of Duty title which the loot season originates.
        season : int
            Loot season number relative to title.
        platform : callofduty.Platform, optional
            Platform which the loot season is available on (default is PlayStation.)
        language : callofduty.Language, optional
            Language which the loot data should be in (default is English.)

        Returns
        -------
        object
            Season object for the requested Loot Season.
        """

        platform = kwargs.get("platform", Platform.PlayStation)
        language = kwargs.get("language", Language.English)

        VerifyPlatform(platform)
        VerifyLanguage(language)

        data: dict = (
            await self.http.GetLootSeason(
                title.value, season, platform.value, language.value
            )
        )["data"]

        # Loot Season responses don't include these values, so we'll just
        # add them manually.
        data["title"] = title.value
        data["platform"] = platform.value
        data["season"] = season
        data["language"] = language.value

        return Season(self, data)

    async def GetPlayerLoadouts(
        self, platform: Platform, username: str, title: Title, **kwargs
    ) -> List[Loadout]:
        """
        Get a Call of Duty player's loadouts for the specified title and mode.

        Parameters
        ----------
        platform : callofduty.Platform
            Platform to get the player from.
        username : str
            Player's username for the designated platform.
        title : callofduty.Title
            Call of Duty title to get the player's loadouts from.
        mode: callofduty.Mode, optional
            Call of Duty mode to get the player's loadouts from (default is Multiplayer.)

        Returns
        -------
        list
            Array of loadout objects.
        """

        mode: Mode = kwargs.get("mode", Mode.Multiplayer)

        VerifyPlatform(platform)
        VerifyTitle(title)
        VerifyMode(mode, title)

        data: dict = (
            await self.http.GetPlayerLoadouts(
                platform.value, username, title.value, mode.value
            )
        )["data"]

        loadouts: List[Loadout] = []
        for _loadout in data["loadouts"]:
            loadouts.append(Loadout(self, _loadout))

        return loadouts

    async def GetPlayerLoadoutUnlocks(
        self, platform: Platform, username: str, title: Title, **kwargs
    ) -> List[LoadoutItem]:
        """
        Get a Call of Duty player's available loadout unlocks for the specified title and mode.

        Parameters
        ----------
        platform : callofduty.Platform
            Platform to get the player from.
        username : str
            Player's username for the designated platform.
        title : callofduty.Title
            Call of Duty title to get the player's loadouts from.
        mode: callofduty.Mode, optional
            Call of Duty mode to get the player's loadouts from (default is Multiplayer.)

        Returns
        -------
        list
            Array of loadout item objects.
        """

        mode: Mode = kwargs.get("mode", Mode.Multiplayer)

        VerifyPlatform(platform)
        VerifyTitle(title)
        VerifyMode(mode, title)

        data: dict = (
            await self.http.GetPlayerLoadouts(
                platform.value, username, title.value, mode.value
            )
        )["data"]

        unlocks: List[LoadoutItem] = []
        for unlock in data["availableUnlocks"]:
            unlocks.append(LoadoutItem(self, {"id": unlock}))

        return unlocks

    async def GetAuthenticityStamp(
        self, platform: Platform, username: str, phrase: str, **kwargs
    ) -> dict:
        """
        Get a Call of Duty Authenticity Stamp for the specified player and phrase.

        Parameters
        ----------
        platform : callofduty.Platform
            Platform to get the player from.
        username : str
            Player's username for the designated platform.
        phrase : str
            Authenticity Stamp code.
        title : callofduty.Title, optional
            Call of Duty title to get the Authenticity Stamp from (default is Black Ops 4.)

        Returns
        -------
        dict
            JSON data for the requested Authenticity Stamp.
        """

        title: Title = kwargs.get("title", Title.BlackOps4)

        VerifyPlatform(platform)
        VerifyTitle(title)

        return (
            await self.http.GetAuthenticityStamp(
                platform.value, username, phrase, title.value
            )
        )["data"]

    async def GetSquad(self, name: str) -> Squad:
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

    async def GetPlayerSquad(self, platform: Platform, username: str) -> Squad:
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

    async def GetMySquad(self) -> Squad:
        """
        Get the Squad of the authenticated Call of Duty player.

        Returns
        -------
        object
            Squad object for the requested Squad.
        """

        return Squad(self, (await self.http.GetMySquad())["data"])

    async def JoinSquad(self, name: str):
        """
        Join a Call of Duty Squad using its name.

        Parameters
        ----------
        name : str
            Name of Squad.
        """

        await self.http.JoinSquad(name)

    async def LeaveSquad(self) -> Squad:
        """
        Leave the Call of Duty Squad of the authenticated player.
        Upon leaving a Squad, the player is automatically placed into
        a random Squad.

        Returns
        -------
        object
            Squad object for the randomly-joined Squad.
        """

        await self.http.LeaveSquad()

        return await self.GetMySquad()
