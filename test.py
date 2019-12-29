import asyncio
import os

import callofduty
from callofduty import GameMode, GameType, Mode, Platform, TimeFrame, Title


async def main():
    client = await callofduty.Login(
        os.environ["ATVI_EMAIL"], os.environ["ATVI_PASSWORD"]
    )

    # season = await client.GetLootSeason(Title.ModernWarfare, 1)
    # print(season["categoryTitle"])
    # for i in season["tiers"]:
    #     itemName = season["tiers"][i]["label"]
    #     itemRarity = season["tiers"][i]["rarity"]
    #     itemType = season["tiers"][i]["type"]
    #     print(f"{itemName} ({itemRarity} {itemType})")

    # requests = await client.GetMyFriendRequests()
    # for incoming in requests["incoming"]:
    #     print(f"Incoming Friend Request: {incoming.username} ({incoming.platform})")
    # for outgoing in requests["outgoing"]:
    #     print(f"Outgoing Friend Request: {outgoing.username} ({outgoing.platform})")

    # friends = await client.GetMyFriends()
    # for friend in friends:
    #     print(f"{friend.platform.name}: {friend.username} ({friend.accountId}), Online? {friend.online}")
    #     for identity in friend.identities:
    #         print(f" - {identity.platform.name}: {identity.username} ({identity.accountId})")

    # identities = await client.GetMyIdentities()
    # for identity in identities:
    #     title = identity["title"].name
    #     username = identity["username"]
    #     platform = identity["platform"].name
    #     print(f"{title}: {username} ({platform})")

    # accounts = await client.GetMyAccounts()
    # for account in accounts:
    #     print(f"{account.username} ({account.platform.name})")

    # player = await client.GetPlayer(Platform.BattleNet, "Mxtive#1930")
    # print(f"{player.username} ({player.platform})")

    # news = await client.GetNewsFeed()
    # for post in news["blog"][:10]:
    #     print(post["title"])

    # leaderboard = await client.GetLeaderboard(
    #     Title.ModernWarfare, Platform.BattleNet, gameMode=GameMode.CyberAttack, page=3
    # )
    # print((leaderboard.entries)[0])
    # for player in await leaderboard.players():
    #     print(f"{player.username} ({player.platform})")

    # leaderboard = await client.GetPlayerLeaderboard(
    #     Title.BlackOps4, Platform.BattleNet, "Mxtive#1930"
    # )
    # print((leaderboard.entries)[0])

    # player = await client.GetPlayer(Platform.Steam, "RdJokr")
    # leaderboard = await player.leaderboard(Title.WWII)
    # print((leaderboard.entries)[17])

    # feed = await client.GetFriendFeed()
    # for event in feed["events"][:5]:
    #     print(event["rendered"])

    # maps = await client.GetAvailableMaps(Title.ModernWarfare)
    # for mapName in maps:
    #     print(mapName)
    #     for mode in maps[mapName]:
    #         print(f" - {mode}")

    # matches = await client.GetPlayerMatches(Platform.Activision, "Yeah#8649242", Title.ModernWarfare, Mode.Multiplayer, limit=3)
    # match = (await player.matches(Title.ModernWarfare, Mode.Multiplayer, limit=3))[1]
    # match = await client.GetMatch(Title.ModernWarfare, Platform.Activision, match.id)
    # teams = await match.teams()
    # for team in teams:
    #     for player in team:
    #         print(player.username)
    # details = await match.details()
    # print(details)

    # results = await client.SearchPlayers(Platform.Activision, "Tustin")
    # for player in results:
    #     print(f"{player.username} ({player.platform})")

    # profile = await player.profile(Title.ModernWarfare, Mode.Multiplayer)
    # print(profile)

    # localize = await client.GetLocalize()
    # print(localize)

    # squad = await client.GetSquad("Autists")
    # squad = await client.GetPlayerSquad(Platform.Activision, "Yeah#8649242")
    # squad = await client.GetMySquad()
    # print(f"{squad.name} - {squad.description}")
    # print(f"Owner: {squad.owner.username} ({squad.owner.platform})")
    # for member in squad.members:
    #     if member.username != squad.owner.username:
    #         print(f"Member: {member.username} ({member.platform})")

    # squad = await client.GetMySquad()
    # print(f"Current Squad: {squad.name} - {squad.description} (Members: {len(squad.members)})")

    # print(f"Leaving Squad '{squad.name}''...")
    # squad = await client.LeaveSquad()
    # print(f"Current Squad: {squad.name} - {squad.description} (Members: {len(squad.members)})")

    # squad = await client.GetSquad("Hmmmm")
    # print(f"Joining Squad '{squad.name}'...")
    # await squad.join()
    # squad = await client.GetMySquad()
    # print(f"Current Squad: {squad.name} - {squad.description} (Members: {len(squad.members)})")


    await client.Logout()


asyncio.run(main())
