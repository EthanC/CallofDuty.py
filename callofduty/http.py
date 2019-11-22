import asyncio
import logging
import urllib.parse

import aiohttp

log = logging.getLogger(__name__)


class Request:
    baseUrl = "https://www.callofduty.com/"
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
        req.SetHeader("Authorization", f"bearer {self.auth.AccessToken}")
        req.SetHeader("x_cod_device_id", self.auth.DeviceId)

        async with self.session.request(
            req.method, req.url, headers=req.headers
        ) as res:
            log.debug(f"{res.status} {res.reason} - {res.method} {res.url}")

            data = await res.json()

            if 300 > res.status >= 200:
                return data

    async def CloseSession(self):
        """Close the session connector."""

        await self.session.close()

    async def SearchPlayer(self, platform: str, searchTerm: str):
        return await self.Request(
            Request(
                "GET",
                f"api/papi-client/crm/cod/v2/platform/{platform}/username/{urllib.parse.quote(searchTerm)}/search",
            )
        )

    async def GetProfile(self, platform: str, username: str):
        return await self.Request(
            Request(
                "GET",
                f"api/papi-client/stats/cod/v1/title/mw/platform/{platform}/gamer/{urllib.parse.quote(username)}/profile/type/mp?locale=en",
            )
        )

    async def GetRecentMatches(self, platform: str, username: str):
        return await self.Request(
            Request(
                "GET",
                f"api/papi-client/crm/cod/v2/title/mw/platform/{platform}/gamer/{urllib.parse.quote(username)}/matches/mp/start/0/end/0/details",
            )
        )

    async def GetMatch(self, platform: str, matchId: str):
        return await self.Request(
            Request(
                "GET",
                f"api/papi-client/ce/v1/title/mw/platform/{platform}/match/{matchId}/matchMapEvents",
            )
        )
