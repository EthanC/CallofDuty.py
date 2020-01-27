import logging
import urllib.parse
from typing import Union

import httpx

from .errors import Forbidden, HTTPException, NotFound

log = logging.getLogger(__name__)


async def JSONorText(res: httpx.Response) -> Union[dict, str]:
    """
    Determine the media type of the provided response.

    Parameters
    ----------
    res : httpx.Response
        Response object to determine media type.

    Returns
    -------
    object
        If media type is JSON data, return dict. Otheriwse return data as str.
    """

    if res.headers["Content-Type"].lower() == "application/json;charset=utf-8":
        return res.json()
    else:
        return res.text()


class Request:
    """Represents a Request object."""

    defaultBaseUrl: str = "https://callofduty.com/"
    squadsBaseUrl: str = "https://squads.callofduty.com/"

    accessToken: str = None
    deviceId: str = None

    def __init__(self, method: str, endpoint: str = None, **kwargs):
        self.method: str = method
        self.headers: dict = {}

        if endpoint is not None:
            baseUrl: str = kwargs.get("baseUrl", self.defaultBaseUrl)
            self.url: str = f"{baseUrl}{endpoint}"

        headers: dict = kwargs.get("headers")
        if isinstance(headers, dict):
            self.headers.update(headers)

    def SetHeader(self, key: str, value: str):
        self.headers[key] = value


class HTTP:
    """HTTP client used to communicate with the Call of Duty API."""

    def __init__(self, auth):
        self.auth = auth
        self.session: httpx.AsyncClient = auth.session

    async def Request(self, req: Request):
        req.SetHeader("Authorization", f"Bearer {self.auth.AccessToken}")
        req.SetHeader("x_cod_device_id", self.auth.DeviceId)

        async with self.session as client:
            res: httpx.Response = await client.request(
                req.method, req.url, headers=req.headers
            )

            data: Union[dict, str] = await JSONorText(res)
            if isinstance(data, dict):
                status: str = data.get("status")

                # The API tends to return HTTP 200 even when an error occurs
                if status == "error":
                    raise HTTPException(res, data)

            # HTTP 2XX: Success
            if 300 > res.status_code >= 200:
                return data

            # HTTP 429: Too Many Requests
            if res.status_code == 429:
                # TODO Handle rate limiting
                raise HTTPException(res, data)

            # HTTP 500/502: Internal Server Error/Bad Gateway
            if res.status_code == 500 or res.status_code == 502:
                # TODO Handle Unconditional retries
                raise HTTPException(res, data)

            # HTTP 403: Forbidden
            if res.status_code == 403:
                raise Forbidden(res, data)
            # HTTP 404: Not Found
            elif res.status_code == 404:
                raise NotFound(res, data)
            else:
                raise HTTPException(res, data)

    async def GetAppLocalize(self, language: str) -> dict:
        return await self.Request(
            Request(
                "GET",
                f"content/atvi/callofduty/mycod/web/{language}/data/json/iq-content-xapp.js",
            )
        )

    async def GetWebLocalize(self, language: str) -> dict:
        return await self.Request(
            Request(
                "GET",
                f"content/atvi/callofduty/mycod/web/{language}/data/json/iq-content-xweb.js",
            )
        )

    async def GetNewsFeed(self, language: str) -> dict:
        return await self.Request(Request("GET", f"site/cod/franchiseFeed/{language}"))

    async def GetFriendFeed(self) -> dict:
        return await self.Request(
            Request("GET", "api/papi-client/userfeed/v1/friendFeed/rendered/")
        )

    async def GetMyIdentities(self) -> dict:
        return await self.Request(
            Request("GET", "api/papi-client/crm/cod/v2/identities/")
        )

    async def GetMyAccounts(self) -> dict:
        return await self.Request(
            Request("GET", "api/papi-client/crm/cod/v2/accounts/")
        )

    async def GetMyFriends(self) -> dict:
        return await self.Request(
            Request("GET", "api/papi-client/codfriends/v1/compendium")
        )

    async def SearchPlayer(self, platform: str, username: str) -> dict:
        return await self.Request(
            Request(
                "GET",
                f"api/papi-client/crm/cod/v2/platform/{platform}/username/{urllib.parse.quote(username)}/search",
            )
        )

    async def GetPlayerProfile(
        self, platform: str, username: str, title: str, mode: str
    ) -> dict:
        return await self.Request(
            Request(
                "GET",
                f"api/papi-client/stats/cod/v1/title/{title}/platform/{platform}/gamer/{urllib.parse.quote(username)}/profile/type/{mode}",
            )
        )

    async def GetPlayerMatches(
        self,
        platform: str,
        username: str,
        title: str,
        mode: str,
        limit: int,
        startTimestamp: int,
        endTimeStamp: int,
    ) -> dict:
        return await self.Request(
            Request(
                "GET",
                f"api/papi-client/crm/cod/v2/title/{title}/platform/{platform}/gamer/{urllib.parse.quote(username)}/matches/{mode}/start/{startTimestamp}/end/{endTimeStamp}?limit={limit}",
            )
        )

    async def GetPlayerMatchesDetailed(
        self,
        platform: str,
        username: str,
        title: str,
        mode: str,
        limit: int,
        startTimestamp: int,
        endTimeStamp: int,
    ) -> dict:
        return await self.Request(
            Request(
                "GET",
                f"api/papi-client/crm/cod/v2/title/{title}/platform/{platform}/gamer/{urllib.parse.quote(username)}/matches/{mode}/start/{startTimestamp}/end/{endTimeStamp}/details?limit={limit}",
            )
        )

    async def GetMatch(self, title: str, platform: str, matchId: int) -> dict:
        return await self.Request(
            Request(
                "GET",
                f"api/papi-client/ce/v1/title/{title}/platform/{platform}/match/{matchId}/matchMapEvents",
            )
        )

    async def GetLeaderboard(
        self,
        title: str,
        platform: str,
        gameType: str,
        gameMode: str,
        timeFrame: str,
        page: int,
    ) -> dict:
        return await self.Request(
            Request(
                "GET",
                f"api/papi-client/leaderboards/v2/title/{title}/platform/{platform}/time/{timeFrame}/type/{gameType}/mode/{gameMode}/page/{page}",
            )
        )

    async def GetPlayerLeaderboard(
        self,
        title: str,
        platform: str,
        username: str,
        gameType: str,
        gameMode: str,
        timeFrame: str,
    ) -> dict:
        return await self.Request(
            Request(
                "GET",
                f"api/papi-client/leaderboards/v2/title/{title}/platform/{platform}/time/{timeFrame}/type/{gameType}/mode/{gameMode}/gamer/{urllib.parse.quote(username)}",
            )
        )

    async def GetAvailableMaps(self, title: str, platform: str, mode: str) -> dict:
        return await self.Request(
            Request(
                "GET",
                f"api/papi-client/ce/v1/title/{title}/platform/{platform}/gameType/{mode}/communityMapData/availability",
            )
        )

    async def GetLootSeason(
        self, title: str, season: int, platform: str, language: str
    ) -> dict:
        return await self.Request(
            Request(
                "GET",
                f"api/papi-client/loot/title/{title}/platform/{platform}/list/loot_season_{season}/{language}",
            )
        )

    async def GetSquad(self, name: str) -> dict:
        return await self.Request(
            Request(
                "GET",
                f"api/v2/squad/lookup/name/{urllib.parse.quote(name)}",
                baseUrl=Request.squadsBaseUrl,
            )
        )

    async def GetPlayerSquad(self, platform: str, username: str) -> dict:
        return await self.Request(
            Request(
                "GET",
                f"api/v2/squad/lookup/platform/{platform}/gamer/{urllib.parse.quote(username)}",
                baseUrl=Request.squadsBaseUrl,
            )
        )

    async def GetMySquad(self) -> dict:
        return await self.Request(
            Request("GET", "api/v2/squad/lookup/mine/", baseUrl=Request.squadsBaseUrl)
        )

    async def JoinSquad(self, name: str) -> dict:
        return await self.Request(
            Request(
                "GET",
                f"api/v2/squad/join/{urllib.parse.quote(name)}",
                baseUrl=Request.squadsBaseUrl,
            )
        )

    async def LeaveSquad(self) -> dict:
        return await self.Request(
            Request("GET", "api/v2/squad/leave/", baseUrl=Request.squadsBaseUrl)
        )
