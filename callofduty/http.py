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
    defaultBaseUrl = "https://callofduty.com/"

    accessToken = None
    deviceId = None

    def __init__(self, method: str, endpoint: str = None, **kwargs):
        self.method = method
        self.headers = {}

        if endpoint is not None:
            baseUrl = kwargs.get("baseUrl", self.defaultBaseUrl)
            self.url = f"{baseUrl}{endpoint}"

        headers = kwargs.get("headers")
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

    async def GetProfile(self, title: str, platform: str, username: str, mode: str):
        return await self.Request(
            Request(
                "GET",
                f"api/papi-client/stats/cod/v1/title/{title}/platform/{platform}/gamer/{urllib.parse.quote(username)}/profile/type/{mode}",
            )
        )

    async def GetRecentMatches(
        self,
        title: str,
        platform: str,
        username: str,
        mode: str,
        limit: int,
        startTimestamp: int,
        endTimeStamp: int,
    ):
        return await self.Request(
            Request(
                "GET",
                f"api/papi-client/crm/cod/v2/title/{title}/platform/{platform}/gamer/{urllib.parse.quote(username)}/matches/{mode}/start/{startTimestamp}/end/{endTimeStamp}?limit={limit}",
            )
        )

    async def GetMatch(self, title: str, platform: str, matchId: int):
        return await self.Request(
            Request(
                "GET",
                f"api/papi-client/ce/v1/title/{title}/platform/{platform}/match/{matchId}/matchMapEvents",
            )
        )

    async def GetAppLocalize(self, language: str):
        return await self.Request(
            Request(
                "GET",
                f"content/atvi/callofduty/mycod/web/{language}/data/json/iq-content-xapp.js",
            )
        )

    async def GetWebLocalize(self, language: str):
        return await self.Request(
            Request(
                "GET",
                f"content/atvi/callofduty/mycod/web/{language}/data/json/iq-content-xweb.js",
            )
        )

    async def GetSquadChallenges(self):
        return await self.Request(
            Request(
                "GET",
                "api/v2/challenge/lookup/current",
                baseUrl="https://squads.callofduty.com/",
            )
        )

    async def SearchSquad(self, query: str):
        return await self.Request(
            Request(
                "GET",
                f"api/v2/squad/lookup/name/{urllib.parse.quote(query)}",
                baseUrl="https://squads.callofduty.com/",
            )
        )
