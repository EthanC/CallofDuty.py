import asyncio
import os

import callofduty
from callofduty.errors import UserNotFound


async def main():
    client = await callofduty.Login(
        os.environ["ATVI_EMAIL"], os.environ["ATVI_PASSWORD"]
    )

    try:
        user = await client.user(callofduty.Platform("uno"), "Tustin#1365515")
    except UserNotFound:
        print("error")
    # users = await client.search(callofduty.Platform.Activision, "Tustin")

    # for u in users:
    #     matches = await u.matches()
    #     # Maybe throw an exception instead? or return an empty list?
    #     if matches == None:
    #         continue
    #     for match in matches:
    #         print(len(await match.teams()))

    # Temporary
    await client.http.CloseSession()


asyncio.run(main())
