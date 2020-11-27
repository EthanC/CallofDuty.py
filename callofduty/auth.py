import logging
import random
from typing import Dict, Optional, Union

import httpx

from .client import Client
from .errors import LoginFailure
from .http import HTTP

log: logging.Logger = logging.getLogger(__name__)


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

    loginUrl: str = "https://profile.callofduty.com/cod/mapp/login"
    registerDeviceUrl: str = "https://profile.callofduty.com/cod/mapp/registerDevice"

    _accessToken: Optional[str] = None
    _deviceId: Optional[str] = None

    def __init__(self, email: str, password: str):
        self.email: str = email
        self.password: str = password
        
        self.session: httpx.AsyncClient = httpx.AsyncClient()

    @property
    def AccessToken(self) -> Optional[str]:
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
    def DeviceId(self) -> Optional[str]:
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
        Generate and register a Device ID with the Call of Duty API. Set
        the corresponding Access Token if successful.
        """

        self._deviceId: Optional[str] = hex(random.getrandbits(128)).lstrip("0x")

        body: Dict[str, Optional[str]] = {"deviceId": self.DeviceId}

        async with self.session as client:
            res: httpx.Response = await client.post(self.registerDeviceUrl, json=body)

            if res.status_code != 200:
                raise LoginFailure(
                    f"Failed to register fake device (HTTP {res.status_code})"
                )

            data: Union[dict, list] = res.json()

            self._accessToken: Optional[str] = dict(data)["data"]["authHeader"]

    async def SubmitLogin(self):
        """
        Submit the specified login credentials to the Call of Duty API using the
        previously acquired Access Token and Device ID.
        """

        headers: Dict[str, str] = {
            "Authorization": f"Bearer {self.AccessToken}",
            "x_cod_device_id": self.DeviceId,
        }

        data: Dict[str, str] = {"email": self.email, "password": self.password}

        async with self.session as client:
            res: httpx.Response = await client.post(
                self.loginUrl, json=data, headers=headers
            )

            if res.status_code != 200:
                raise LoginFailure(f"Failed to login (HTTP {res.status_code})")


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
