import asyncio
import logging

from .enums import Platform
from .errors import CallofDutyException

import callofduty.user

log = logging.getLogger(__name__)

class Client:
    def __init__(self, http):
        self.http = http

    def __aenter__(self):
        return self

    async def __aexit__(self, exType, exValue, exTraceback):
        await self.CloseSession()

    async def CloseSession(self):
        await self.http.CloseSession()

    async def SearchPlayer(self, platform: Platform, username: str):
        if platform not in Platform:
            raise CallofDutyException("Invalid platform specified")

        data = await self.http.SearchPlayer(platform.value, username)

        users = []

        for user in data['data']:
            users.append(callofduty.User(self.http, user))

        return users
