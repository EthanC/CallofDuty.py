import logging

from .enums import Mode, Platform, Title
from .errors import InvalidMode, InvalidProfile, InvalidTitle

log = logging.getLogger(__name__)


class User:
    def __init__(
        self,
        http: object,
        platform: str,
        username: str,
        accountId: int = None,
        avatarUrls: list = None,
    ):
        self.http = http
        self.platform = Platform(platform)
        self.username = username
        self.accountId = accountId
        self.avatarUrls = avatarUrls

    async def profile(self, title: Title, mode: Mode):
        if title not in Title:
            raise InvalidTitle(f"{title} is not a valid title")

        if mode not in Mode:
            # TODO Validate mode for title
            # e.g. Zombies is not a valid mode for Modern Warfare
            raise InvalidMode(f"{mode} is not a valid mode")

        profile = await self.http.GetProfile(
            title.value, self.platform.value, self.username, mode.value
        )

        return profile["data"]

    async def matches(
        self, title: Title, mode: Mode, limit: int = 10, lazy: bool = True
    ):
        from .match import Match

        if title not in Title:
            raise InvalidTitle(f"{title} is not a valid title")

        if mode not in Mode:
            # TODO Validate mode for title
            # e.g. Zombies is not a valid mode for Modern Warfare
            raise InvalidMode(f"{mode} is not a valid mode")

        data = await self.http.GetRecentMatches(
            title.value, self.platform.value, self.username, mode.value, limit
        )

        matches = []

        for i in data["data"]:
            _match = Match(self.http, title, self.platform, i)
            matches.append(_match)

            # For clarity
            if lazy == False:
                _match.teams()

        return matches
