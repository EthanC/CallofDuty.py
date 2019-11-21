import asyncio
import os

import callofduty

async def main():
    client = await callofduty.Login(os.environ['ATVI_EMAIL'], os.environ['ATVI_PASSWORD'])

    users = await client.SearchPlayer(callofduty.Platform.Activision, "Tustin")

    for u in users:
        matches = await u.matches()
        # Maybe throw an exception instead? or return an empty list?
        if matches == None:
            continue
        for match in matches:
            print(len(await match.teams()))

    # Temporary
    await client.http.CloseSession()


asyncio.run(main())