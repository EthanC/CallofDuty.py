import asyncio
import os

import callofduty
from callofduty import GameMode, GameType, Mode, Platform, TimeFrame, Title


async def main():
    client = await callofduty.Login(
        os.environ["ATVI_EMAIL"], os.environ["ATVI_PASSWORD"]
    )

    # friends = await client.GetMyFriends()
    # for friend in friends:
    #     print(f"{friend.platform.name}: {friend.username} ({friend.accountId}), Online? {friend.online}")

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

    # matches = await client.GetPlayerMatches(Platform.Activision, "Yeah#8649242", Title.ModernWarfare, Mode.Multiplayer, limit=3)
    # match = (await player.matches(Title.ModernWarfare, Mode.Multiplayer, limit=3))[1]
    # match = await client.GetMatch(Title.ModernWarfare, Platform.Activision, Mode.Multiplayer, match.id)
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

    # match = (await user.matches(Title.ModernWarfare, Mode.Multiplayer))[0]
    # teams = await match.teams()
    # for team in teams:
    #     for player in team:
    #         print(player.username)

    # localize = await client.GetLocalize()
    # print(localize)

    # challenge = await client.GetSquadChallenges()
    # print(challenge)

    # squad = await client.GetSquad("Autists")
    # squad = await client.GetPlayerSquad(Platform.Activision, "Yeah#8649242")
    # squad = await client.GetMySquad()
    # print(f"{squad.name} - {squad.description}")
    # print(f"Owner: {squad.owner.username} ({squad.owner.platform})")
    # for member in squad.members:
    #     if member.username != squad.owner.username:
    #         print(f"Member: {member.username} ({member.platform})")

    await client.Logout()


asyncio.run(main())
