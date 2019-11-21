import asyncio
import os
import callofduty


async def main():
    auth = await callofduty.Login(os.environ['ATVI_EMAIL'], os.environ['ATVI_PASSWORD'])
    client = callofduty.Client(auth)

    data = await client.SearchPlayer(callofduty.Platform.Activision, "Tustin")

    print(data)

    # Temporary
    await client.http.CloseSession()


asyncio.run(main())