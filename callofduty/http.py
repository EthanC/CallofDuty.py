import asyncio
import logging

import aiohttp

# from .errors import *

log = logging.getLogger(__name__)


class Request:
    baseUrl = "https://callofduty.com/"
    accessToken = None
    deviceId = None

    def __init__(self, method: str, endpoint: str = None, headers: dict = None):
        self.method = method
        self.headers = {}

        if endpoint is not None:
            self.url = f"{self.baseUrl}{endpoint}"

        if isinstance(headers, dict):
            self.headers.update(headers)

    def SetHeader(self, key: str, value: str):
        """ToDo"""

        self.headers[key] = value


class HTTP:
    def __init__(self, auth):
        self.auth = auth
        self.session = auth.session

    async def Request(self, req):
        """ToDo"""

        req.SetHeader("Authorization", f"bearer {self.auth.AccessToken}")
        req.SetHeader("x_cod_device_id", self.auth.DeviceId)

        async with self.session.request(
            req.method, req.url, headers=req.headers
        ) as res:
            log.debug(f"{res.status} {res.reason} - {res.method} {res.url}")

            data = await res.text()

            if 300 > res.status >= 200:
                return data

    async def CloseSession(self):
        """ToDo"""

        await self.session.close()

    async def SearchPlayer(self, platform: str, username: str):
        """ToDo"""

        return await self.Request(
            Request(
                "GET",
                f"api/papi-client/crm/cod/v2/platform/{platform}/username/{username}/search",
            )
        )
