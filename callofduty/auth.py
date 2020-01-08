import asyncio
import logging
import random

import aiohttp

from .client import Client
from .errors import LoginFailure
from .http import HTTP

log = logging.getLogger(__name__)


class Auth:
    """
    Implements the Call of Duty authorization flow.

    Parameters
    ----------
    email : str
        Activision account email address.
    password : str
        Activision account password.
    """

    loginUrl = "https://profile.callofduty.com/cod/mapp/login"
    registerDeviceUrl = "https://profile.callofduty.com/cod/mapp/registerDevice"

    _accessToken: str = None
    _deviceId: str = None

    def __init__(self, email: str, password: str):
        self.email: str = email
        self.password: str = password

        self.loop = asyncio.get_event_loop()
        self.cookieJar = aiohttp.CookieJar()
        self.session = aiohttp.ClientSession(loop=self.loop, cookie_jar=self.cookieJar)

    @property
    def AccessToken(self) -> str:
        """
        Returns
        -------
        str
            Access Token which is set during the device registration phase
            of authentication.
        """

        if self._accessToken is None:
            raise LoginFailure("Access Token is null, not authenticated")

        return self._accessToken

    @property
    def DeviceId(self) -> str:
        """
        Returns
        -------
        str
            Device ID which is set during the device registration phase
            of authentication.
        """

        if self._deviceId is None:
            raise LoginFailure("DeviceId is null, not authenticated")

        return self._deviceId

    async def RegisterDevice(self):
        """
        Generate and register a Device ID with the Call of Duty API.

        Set the corresponding Access Token if successful.
        """

        self._deviceId: str = hex(random.getrandbits(128)).lstrip("0x")

        body: dict = {"deviceId": self.DeviceId}

        async with self.session.post(self.registerDeviceUrl, json=body) as res:
            if res.status != 200:
                raise LoginFailure(
                    f"Failed to register fake device (HTTP {res.status} {res.reason})"
                )

            data: dict = await res.json()

            self._accessToken = data["data"]["authHeader"]

    async def SubmitLogin(self):
        """
        Submit the specified login credentials to the Call of Duty API using the
        previously acquired Access Token and Device ID.
        """

        headers: dict = {
            "Authorization": f"Bearer {self.AccessToken}",
            "x_cod_device_id": self.DeviceId,
        }

        data: dict = {"email": self.email, "password": self.password}

        async with self.session.post(self.loginUrl, json=data, headers=headers) as res:
            if res.status != 200:
                raise LoginFailure(f"Failed to login (HTTP {res.status} {res.reason})")


async def Login(email: str, password: str) -> Client:
    """
    Convenience function to make login with the Call of Duty authorization flow
    as easy as possible.

    Parameters
    ----------
    email : str
        Activision account email address.
    password : str
        Activision account password.

    Returns
    -------
    object
        Authenticated Call of Duty client.
    """

    auth: Auth = Auth(email, password)

    await auth.RegisterDevice()
    await auth.SubmitLogin()

    return Client(HTTP(auth))
