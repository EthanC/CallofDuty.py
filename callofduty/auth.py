import asyncio
import json
import logging
import random

import aiohttp

from .client import Client
from .errors import LoginFailure
from .http import HTTP

log = logging.getLogger(__name__)


class Auth:
    loginUrl = "https://profile.callofduty.com/cod/mapp/login"
    registerDeviceUrl = "https://profile.callofduty.com/cod/mapp/registerDevice"

    _accessToken = None
    _deviceId = None

    def __init__(self, email: str, password: str, loop=None):
        self.email = email
        self.password = password
        self.loop = loop or asyncio.get_event_loop()
        self.cookieJar = aiohttp.CookieJar()

        self.session = aiohttp.ClientSession(loop=self.loop, cookie_jar=self.cookieJar)

    @property
    def AccessToken(self):
        if self._accessToken is None:
            raise LoginFailure("Access Token is null, not authenticated")

        return self._accessToken

    @property
    def DeviceId(self):
        if self._deviceId is None:
            raise LoginFailure("DeviceId is null, not authenticated")

        return self._deviceId

    async def GetLoginCookies(self):
        """Set the session cookies necessary for login."""

        await self.session.get(self.loginUrl)

    def GenerateDeviceId(self):
        """Return a randomly generated 32 character Device ID."""

        return hex(random.getrandbits(128)).lstrip("0x")

    async def RegisterDevice(self, deviceId: str):
        """
        Register the specified Device ID with the Call of Duty API.

        Return the corresponding Access Token if successful.
        """

        body = {"deviceId": deviceId}

        async with self.session.post(self.registerDeviceUrl, json=body) as res:
            if res.status != 200:
                raise LoginFailure(
                    f"Failed to register fake device (HTTP {res.status} {res.reason})"
                )

            data = await res.json()

            return data["data"]["authHeader"]

    def SetAccessToken(self, accessToken: str):
        """Set the Access Token to be used across all requests."""

        self._accessToken = accessToken

    def SetDeviceId(self, deviceId: str):
        """Set the Device ID to be used across all requests."""

        self._deviceId = deviceId

    async def SubmitLogin(self, email: str, password: str):
        """
        Submit the specified login credentials to the Call of Duty API along with
        the previously acquired Access Token and Device ID.
        """

        headers = {
            "Authorization": f"bearer {self._accessToken}",
            "x_cod_device_id": self._deviceId,
            "Content-Type": "application/json",
        }

        data = {"email": email, "password": password}

        async with self.session.post(self.loginUrl, json=data, headers=headers) as res:
            if res.status != 200:
                raise LoginFailure(f"Failed to login (HTTP {res.status} {res.reason})")


async def Login(email: str, password: str):
    """
    Convenience function to make login with the Call of Duty authorization flow
    as easy as possible.

    Return an authenticated Client if login is successful.
    """

    auth = Auth(email, password)

    await auth.GetLoginCookies()

    deviceId = auth.GenerateDeviceId()
    accessToken = await auth.RegisterDevice(deviceId)

    auth.SetAccessToken(accessToken)
    auth.SetDeviceId(deviceId)

    await auth.SubmitLogin(email, password)

    return Client(HTTP(auth))
