import asyncio
import logging
import urllib.parse

import aiohttp

from .errors import Forbidden, HTTPException, NotFound

log = logging.getLogger(__name__)


async def JSONorText(res: aiohttp.ClientResponse):
    """
    Determine the media type of the provided response.

    Return a dict object for JSON data, otherwise return data as string.
    """

    if res.headers["Content-Type"] == "application/json;charset=UTF-8":
        return await res.json(encoding="utf-8")
    else:
        return await res.text(encoding="utf-8")


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
        self.headers[key] = value


class HTTP:
    """Represents an HTTP client sending HTTP requests to the Call of Duty API."""

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

            data = await JSONorText(res)

            if isinstance(data, dict):
                status = data.get("status")

                # The API tends to return HTTP 200 even when an error occurs
                if status == "error":
                    raise HTTPException(res, data)

            # HTTP 2XX: Success
            if 300 > res.status >= 200:
                return data

            # HTTP 429: Too Many Requests
            if res.status == 429:
                # TODO Handle rate limiting
                raise HTTPException(res, data)

            # HTTP 500/502: Internal Server Error/Bad Gateway
            if res.status == 500 or res.status == 502:
                # TODO Handle Unconditional retries
                raise HTTPException(res, data)

            # HTTP 403: Forbidden
            if res.status == 403:
                raise Forbidden(res, data)
            # HTTP 404: Not Found
            elif res.status == 404:
                raise NotFound(res, data)
            else:
                raise HTTPException(res, data)

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
