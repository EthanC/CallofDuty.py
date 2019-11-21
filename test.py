import asyncio
import os

import callofduty

async def main():
    client = await callofduty.Login(os.environ['ATVI_EMAIL'], os.environ['ATVI_PASSWORD'])

    users = await client.SearchPlayer(callofduty.Platform.Activision, "Tustin")

    for u in users:
        print(await u.profile())

    # Temporary
    await client.http.CloseSession()


asyncio.run(main())