import asyncio
import logging

from .enums import Language, Platform
from .errors import InvalidLanguage, InvalidPlatform, InvalidProfile, UserNotFound
from .squad import Squad
from .user import User

log = logging.getLogger(__name__)


class Client:
    def __init__(self, http: object):
        self.http = http

    def __aenter__(self):
        return self

    async def __aexit__(self, exType, exValue, exTraceback):
        await self.CloseSession()

    async def CloseSession(self):
        """Close the session connector."""

        await self.http.CloseSession()

    async def user(self, platform: Platform, username: str):
        if platform not in Platform:
            raise InvalidPlatform(f"{platform} is not a valid platform")

        return User(self.http, platform.value, username)

    async def search(self, platform: Platform, username: str, limit: int = 0):
        if platform not in Platform:
            raise InvalidPlatform(f"{platform} is not a valid platform")

        data = await self.http.SearchPlayer(platform.value, username)

        if limit > 0:
            data["data"] = data["data"][:limit]

        users = []

        for user in data["data"]:
            accountId = user.get("accountId")
            if isinstance(accountId, str):
                # The API returns the accountId as a string
                accountId = int(accountId)

            if isinstance(user["avatar"], dict):
                avatarUrls = []
                for key in user["avatar"]:
                    avatarUrls.append(user["avatar"][key])
            else:
                avatarUrls = None

            users.append(
                User(
                    self.http,
                    platform=user["platform"],
                    username=user["username"],
                    accountId=accountId,
                    avatarUrls=avatarUrls,
                )
            )

        return users

    async def GetAppLocalize(self, language: Language = Language.English):
        if language not in Language:
            raise InvalidLanguage(f"{language} is not a valid language")

        data = await self.http.GetAppLocalize(language.value)

        return data

    async def GetWebLocalize(self, language: Language = Language.English):
        if language not in Language:
            raise InvalidLanguage(f"{language} is not a valid language")

        data = await self.http.GetAppLocalize(language.value)

        return data

    async def GetSquadChallenges(self, language: Language = Language.English):
        if language not in Language:
            raise InvalidLanguage(f"{language} is not a valid language")

        data = await self.http.GetSquadChallenges()

        return data

    async def SearchSquad(self, query: str):
        data = await self.http.SearchSquad(query)

        return data
