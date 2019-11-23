import logging

from .enums import Platform
from .errors import InvalidProfileError
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

    async def profile(self):
        profile = await self.http.GetProfile(self.platform.value, self.username)

        if profile["status"] != "success":
            raise InvalidProfileError(profile["data"].get("message") or "Unknown Error")

        return profile

    async def matches(self, count: int = 0, lazy: bool = True):
        from .match import Match

        data = await self.http.GetRecentMatches(self.platform.value, self.username)

        matches = []

        if data["data"]["matches"] == None:
            return None

        for it in data["data"]["matches"]:
            match = Match(self.http, self.platform, it)
            matches.append(match)

            # For clarity
            if lazy == False:
                match.teams()

        return matches
