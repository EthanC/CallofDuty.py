import asyncio
import logging

from .enums import Platform
from .errors import CallofDutyException
from .http import HTTP

log = logging.getLogger(__name__)


class Client:
    def __init__(self, auth):
        self.auth = auth
        self.http = HTTP(auth)

    def __aenter__(self):
        return self

    async def __aexit__(self, exType, exValue, exTraceback):
        await self.CloseSession()

    async def CloseSession(self):
        """ToDo"""

        await self.http.CloseSession()

    async def SearchPlayer(self, platform: Platform, username: str):
        """ToDo"""

        if platform not in Platform:
            raise CallofDutyException("Invalid platform specified")

        data = await self.http.SearchPlayer(platform.value, username)

        return data
