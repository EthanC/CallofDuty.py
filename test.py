import asyncio
import os

import callofduty
from callofduty import Mode, Platform, Title


async def main():
    client = await callofduty.Login(
        os.environ["ATVI_EMAIL"], os.environ["ATVI_PASSWORD"]
    )

    # user = (await client.search(Platform.Activision, "Tustin"))[1]
    # print(f"{user.username} ({user.accountId})")

    # profile = await user.profile(Title.ModernWarfare, Mode.Multiplayer)
    # print(profile)

    # match = (await user.matches(Title.ModernWarfare, Mode.Multiplayer))[0]
    # teams = await match.teams()
    # for team in teams:
    #     for player in team:
    #         print(player.username)

    # localize = await client.GetAppLocalize()
    # print(localize)

    # Temporary
    await client.http.CloseSession()


asyncio.run(main())
