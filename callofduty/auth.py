import asyncio
import json
import logging
import random

import aiohttp

import callofduty.client

from .http import HTTP

from .errors import AuthenticationError, CallofDutyException

log = logging.getLogger(__name__)

class Auth:
    loginUrl = "https://profile.callofduty.com/cod/mapp/login"
    registerDeviceUrl = "https://profile.callofduty.com/cod/mapp/registerDevice"

    _accessToken = None
    _deviceId = None

    def __init__(self, email: str, password: str, loop=None):
        self.email = email
        self.password = password

        self.session = aiohttp.ClientSession(
            loop=loop or asyncio.get_event_loop(), cookie_jar=aiohttp.CookieJar()
        )

    @property
    def AccessToken(self):
        if self._accessToken is None:
            raise AuthenticationError("Access Token is null, not authenticated")

        return self._accessToken

    @property
    def DeviceId(self):
        if self._deviceId is None:
            raise AuthenticationError("DeviceId is null, not authenticated")

        return self._deviceId

    async def GetLoginCookies(self):
        await self.session.get(self.loginUrl)

    def GenerateDeviceId(self):
        return hex(random.getrandbits(128)).lstrip('0x')

    async def RegisterDevice(self, deviceId: str):
        body = {"deviceId": deviceId}

        async with self.session.post(self.registerDeviceUrl, json=body) as res:
            if res.status != 200:
                raise AuthenticationError(f"Failed to register fake device: {res.status}")

            data = await res.json()

            return data['data']['authHeader']

    def SetAccessToken(self, accessToken: str):
        self._accessToken = accessToken

    def SetDeviceId(self, deviceId: str):
        self._deviceId = deviceId

    async def SubmitLogin(self, email: str, password: str):
        headers = {
            "Authorization": f"bearer {self._accessToken}",
            "x_cod_device_id": self._deviceId,
            "Content-Type": "application/json",
        }

        data = {"email": email, "password": password}

        async with self.session.post(self.loginUrl, json=data, headers=headers) as res:
            if res.status != 200:
                raise AuthenticationError(f"Failed to login: {res.status}")


async def Login(email: str, password: str):
    auth = Auth(email, password)

    await auth.GetLoginCookies()

    deviceId = auth.GenerateDeviceId()
    accessToken = await auth.RegisterDevice(deviceId)

    auth.SetAccessToken(accessToken)
    auth.SetDeviceId(deviceId)

    await auth.SubmitLogin(email, password)

    return callofduty.Client(HTTP(auth))
