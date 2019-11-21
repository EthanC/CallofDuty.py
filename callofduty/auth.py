import asyncio
import json
import logging
from uuid import uuid4

import aiohttp

from .errors import AuthenticationError, CallofDutyException

log = logging.getLogger(__name__)


class Auth:
    """ToDo"""

    loginUrl = "https://profile.callofduty.com/cod/login"
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

    # async def testing(self):
    #     bbb = self.session.cookie_jar.__len__()
    #     print(bbb)

    #     for yeah in self.session.cookie_jar._cookies:
    #         print(yeah)

    async def GetLoginCookies(self):
        """ToDo"""

        await self.session.get(self.loginUrl)

        # aaa = self.session.cookie_jar.__len__()

        # print(aaa)

        # for yeah in self.session.cookie_jar:
        #     print(yeah)

    def GenerateDeviceId(self):
        """ToDo"""

        return uuid4().hex[:16].lower()

    async def RegisterDevice(self, deviceId: str):
        """ToDo"""

        data = {"deviceId": deviceId}

        async with self.session.post(self.registerDeviceUrl, json=data) as res:
            if res.status != 200:
                raise AuthenticationError(f"Failed to register device with ID: {deviceId}")

            data = await res.json()

            accessToken = json.loads(json.dumps(data))["data"]["authHeader"]

            return accessToken

    def SetAccessToken(self, accessToken: str):
        """ToDo"""

        self._accessToken = accessToken

    def SetDeviceId(self, deviceId: str):
        """ToDo"""

        self._deviceId = deviceId

    async def SubmitLogin(self, email: str, password: str):
        """ToDo"""

        headers = {
            "Authorization": f"bearer {self._accessToken}",
            "x_cod_device_id": self._deviceId,
            "Content-type": "application/json",
        }
        data = {"email": email, "password": password}

        async with self.session.post(self.loginUrl, json=data, headers=headers) as res:
            # if res.status != 200:
            #     raise AuthenticationError("Failed to login")

            data = await res.text()

            return data


async def Login(email: str, password: str):
    """ToDo"""

    auth = Auth(email, password)

    # await auth.testing()

    await auth.GetLoginCookies()

    deviceId = auth.GenerateDeviceId()
    accessToken = await auth.RegisterDevice(deviceId)

    auth.SetAccessToken(accessToken)
    auth.SetDeviceId(deviceId)

    # print(email)
    # print(password)
    # print(accessToken)
    # print(deviceId)

    test = await auth.SubmitLogin(email, password)

    print(str(test))

    return auth
