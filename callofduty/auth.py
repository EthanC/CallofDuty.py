import logging
import random
from typing import Dict, Optional, Union

import httpx

from .client import Client
from .errors import LoginFailure
from .http import HTTP, JSONorText

log: logging.Logger = logging.getLogger(__name__)


class Auth:
    """
    Implements the Call of Duty authorization flow.

    Parameters
    ----------
    email : str, optional
        Activision account email address.
    password : str, optional
        Activision account password.
    sso : str, optional
        Activision single sign-on cookie value.
    """

    loginUrl: str = "https://profile.callofduty.com/cod/mapp/login"
    registerDeviceUrl: str = "https://profile.callofduty.com/cod/mapp/registerDevice"

    _accessToken: Optional[str] = None
    _deviceId: Optional[str] = None

    def __init__(
        self,
        email: Optional[str] = None,
        password: Optional[str] = None,
        sso: Optional[str] = None,
    ):
        self.email: Optional[str] = email
        self.password: Optional[str] = password
        self.sso: Optional[str] = sso

        self.session: httpx.AsyncClient = httpx.AsyncClient()

        if self.sso is not None:
            self.session.cookies.set("ACT_SSO_COOKIE", self.sso)

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
            elif isinstance(data := await JSONorText(res), dict):
                if data.get("success") is not True:
                    # The API tends to return HTTP 200 even when an error occurs
                    raise LoginFailure(
                        f"Failed to login (HTTP {res.status_code}), "
                        + data.get("token", data)
                    )


async def Login(
    email: Optional[str] = None,
    password: Optional[str] = None,
    sso: Optional[str] = None,
) -> Client:
    """
    Convenience function to make login with the Call of Duty authorization flow
    as easy as possible. Requires one of email and password or sso cookie value.

    Parameters
    ----------
    email : str, optional
        Activision account email address.
    password : str, optional
        Activision account password.
    sso: str, optional
        Activision single sign-on cookie value.

    Returns
    -------
    object
        Authenticated Call of Duty client.
    """

    auth: Auth = Auth(email, password, sso)

    if (email is None) and (sso is None):
        raise LoginFailure("Failed to login, insufficient credentials provided")
    elif (email is not None) and (password is not None):
        await auth.RegisterDevice()
        await auth.SubmitLogin()

        return Client(HTTP(auth))
    elif sso is not None:
        await auth.RegisterDevice()

        return Client(HTTP(auth))
