import asyncio
import os

from dotenv import load_dotenv

import callofduty
from callofduty import Mode, Platform, Title


async def main():
    load_dotenv()
    client = await callofduty.Login(
        os.environ["ATVI_EMAIL"], os.environ["ATVI_PASSWORD"]
    )

    # season = await client.GetLootSeason(Title.BlackOps4, 3)
    # print(f"{season.title.name}: {season.name}")
    # for tier in season.tiers:
    #     print(f"Tier {tier.tier}: {tier.name} - {tier.rarity} {tier.category}")
    # for chase in season.chase:
    #     print(f"Chase: {chase.name} - {chase.rarity} {chase.category}")

    # requests = await client.GetMyFriendRequests()
    # for incoming in requests["incoming"]:
    #     print(f"Incoming Friend Request: {incoming.username} ({incoming.platform.name})")
    # for outgoing in requests["outgoing"]:
    #     print(f"Outgoing Friend Request: {outgoing.username} ({outgoing.platform.name})")

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
    # print(f"{player.username} ({player.platform.name})")

    # player = await client.GetPlayer(Platform.BattleNet, "Mxtive#1930")
    # summary = await player.matchesSummary(Title.ModernWarfare, Mode.Multiplayer, limit=20)
    # print(summary)

    # news = await client.GetNewsFeed(limit=10)
    # for post in news:
    #     print(f"{post.published.date()}: {post.title}")

    # videos = await client.GetVideoFeed(limit=3)
    # for video in videos:
    #     print(f"{video.title} - {video.url}")

    # leaderboard = await client.GetLeaderboard(
    #     Title.ModernWarfare, Platform.BattleNet, gameMode="cyber", page=3
    # )
    # for entry in leaderboard.entries:
    #     print(f"#{entry.rank}: {entry.username} ({entry.platform.name})")

    # leaderboard = await client.GetPlayerLeaderboard(
    #     Title.BlackOps4, Platform.BattleNet, "Mxtive#1930"
    # )
    # for entry in leaderboard.entries:
    #     if entry.username == "Mxtive#1930":
    #         print(f"#{entry.rank}: {entry.username} ({entry.platform.name})")

    # player = await client.GetPlayer(Platform.Steam, "RdJokr")
    # leaderboard = await player.leaderboard(Title.WWII)
    # for entry in leaderboard.entries:
    #     if entry.username == player.username:
    #         print(f"#{entry.rank}: {entry.username} ({entry.platform.name})")

    # feed = await client.GetFriendFeed()
    # for event in feed["events"][:5]:
    #     print(event["rendered"])

    # maps = await client.GetAvailableMaps(Title.ModernWarfare)
    # for mapName in maps:
    #     print(mapName)
    #     for mode in maps[mapName]:
    #         print(f" - {mode}")

    # matches = await client.GetPlayerMatches(Platform.Activision, "Yeah#8649242", Title.ModernWarfare, Mode.Multiplayer, limit=3)
    # for match in matches:
    #     print(match.id)

    # player = await client.GetPlayer(Platform.BattleNet, "Mxtive#1930")
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
    #     print(f"{player.username} ({player.platform.name})")

    # player = await client.GetPlayer(Platform.BattleNet, "Mxtive#1930")
    # profile = await player.profile(Title.ModernWarfare, Mode.Multiplayer)
    # print(profile)

    # localize = await client.GetLocalize()
    # print(localize)

    # loadouts = await client.GetPlayerLoadouts(Platform.PlayStation, "ImMotive__", Title.BlackOps4)
    # for loadout in loadouts:
    #     if loadout.name != "":
    #         print(f"Class: {loadout.name} (Unlocked: {loadout.unlocked})")
    #         if loadout.primary.id is not None:
    #             print(f" - Primary Weapon: {loadout.primary.id} (Variant: {loadout.primary.variant})")
    #             print(f"  - Camo: {loadout.primary.camo}")
    #             for attachment in loadout.primary.attachments:
    #                 if attachment.id is not None:
    #                     print(f"  - Attachment: {attachment.id}")
    #         if loadout.secondary.id is not None:
    #             print(f" - Secondary Weapon: {loadout.secondary.id} (Variant: {loadout.secondary.variant})")
    #             print(f"  - Camo: {loadout.secondary.camo}")
    #             for attachment in loadout.secondary.attachments:
    #                 if attachment.id is not None:
    #                     print(f"  - Attachment: {attachment.id}")
    #         for equipment in loadout.equipment:
    #             if equipment.id is not None:
    #                 print(f" - Equipment: {equipment.id}")
    #         for perk in loadout.perks:
    #             if perk.id is not None:
    #                 print(f" - Perk: {perk.id}")
    #         for wildcard in loadout.wildcards:
    #             if wildcard.id is not None:
    #                 print(f" - Wildcard: {wildcard.id}")

    # player = await client.GetPlayer(Platform.PlayStation, "ImMotive__")
    # loadouts = await player.loadouts(Title.BlackOps4)
    # for loadout in loadouts:
    #     if loadout.name != "":
    #         print(f"Class: {loadout.name} (Unlocked: {loadout.unlocked})")

    # unlocks = await client.GetPlayerLoadoutUnlocks(Platform.PlayStation, "ImMotive__", Title.BlackOps4)
    # for unlock in unlocks:
    #     print(unlock.id)

    # player = await client.GetPlayer(Platform.PlayStation, "ImMotive__")
    # unlocks = await player.loadoutUnlocks(Title.BlackOps4)
    # for unlock in unlocks:
    #     print(unlock.id)

    # stamp = await client.GetAuthenticityStamp(
    #     Platform.BattleNet, "Slicky#21337", "Swiftly Snarling Gamy Generators"
    # )
    # print(stamp.data)

    # player = await client.GetPlayer(Platform.BattleNet, "Slicky#21337")
    # stamp = await player.authenticityStamp("Swiftly Snarling Gamy Generators")
    # print(stamp.stats)

    # req = await client.AddFriend(5273496286943517033)
    # print(f"Friend Request Status: {req}")

    # req = await client.RemoveFriend(13940176918450289589)
    # print(f"Friend Request Status: {req}")

    # results = await client.SearchPlayers(Platform.Activision, "Tustin")
    # for player in results:
    #     print(f"{player.username} ({player.platform.name})")
    #     if player.username == "Tustin#1365515":
    #         req = await player.removeFriend()
    #         print(f"Removed Friend ({req})")
    #         req = await player.addFriend()
    #         print(f"Added Friend ({req})")

    # favs = await client.GetMyFavorites()
    # for favorite in favs:
    #     print(f"Favorite: {favorite.username} ({favorite.platform.name})")

    # favs = await client.AddFavorite(Platform.Activision, "Dad#1869899")
    # print(f"Favorites: {len(favs)}")

    # player = await client.GetPlayer(Platform.Activision, "Dad#1869899")
    # favs = await player.removeFavorite()
    # print(f"Favorites: {len(favs)}")

    # results = await client.SearchPlayers(Platform.Activision, "Tustin")
    # for player in results:
    #     if player.username == "Tustin#1365515":
    #         await player.block()
    #         await player.unblock()
    #         req = await player.addFriend()
    #         print(req)

    # squad = await client.GetSquad("Autists")
    # print(f"{squad.name} - {squad.description}")
    # print(f"Owner: {squad.owner.username} ({squad.owner.platform.name})")
    # for member in squad.members:
    #     if member.username != squad.owner.username:
    #         print(f"Member: {member.username} ({member.platform.name})")

    # squad = await client.GetPlayerSquad(Platform.Activision, "Yeah#8649242")
    # print(f"{squad.name} - {squad.description}")
    # print(f"Owner: {squad.owner.username} ({squad.owner.platform.name})")
    # for member in squad.members:
    #     if member.username != squad.owner.username:
    #         print(f"Member: {member.username} ({member.platform.name})")

    # squad = await client.GetMySquad()
    # print(f"{squad.name} - {squad.description}")
    # print(f"Owner: {squad.owner.username} ({squad.owner.platform.name})")
    # for member in squad.members:
    #     if member.username != squad.owner.username:
    #         print(f"Member: {member.username} ({member.platform.name})")

    # print(f"Leaving Squad '{squad.name}''...")
    # squad = await client.LeaveSquad()
    # print(f"Current Squad: {squad.name} - {squad.description} (Members: {len(squad.members)})")

    # squad = await client.GetSquad("Hmmmm")
    # print(f"Joining Squad '{squad.name}'...")
    # await squad.join()
    # squad = await client.GetMySquad()
    # print(f"Current Squad: {squad.name} - {squad.description} (Members: {len(squad.members)})")

    # squad = await client.GetSquad("Hmmmm")
    # await squad.report()


asyncio.get_event_loop().run_until_complete(main())
