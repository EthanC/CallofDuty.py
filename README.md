# Welcome to CallofDuty.py

 CallofDuty.py is an asynchronous, object-oriented Python wrapper for the Call of Duty API. [![](https://img.shields.io/pypi/v/callofduty.py?label=Version&style=for-the-badge)](https://pypi.python.org/pypi/callofduty.py) [![](https://img.shields.io/pypi/dm/callofduty.py?style=for-the-badge)](https://pypi.python.org/pypi/callofduty.py) [![](https://img.shields.io/twitter/follow/Mxtive?color=1da1f2&label=Twitter&style=for-the-badge)](https://twitter.com/Mxtive) [![](https://img.shields.io/discord/136986169563938816?color=7289DA&label=Discord&style=for-the-badge)](https://discord.gg/callofduty)

## Features

* Fully asynchronous using async and await
* Object-oriented nature allows for ease of use
* More soon...

## Usage

Construct a new Call of Duty client, then use the various services on the client to access different parts of the Call of Duty API.

For complete usage of CallofDuty.py, see the Documentation.

### Installation

CallofDuty.py requires Python 3.7 or higher. Once that requirement is met, simply install CallofDuty.py using pip!

```text
pip install callofduty.py
```

### Example

The following is a complete example which demonstrates:

* Searching for a user
* Listing the first 3 search results
* Getting the profile of the second result
* Displaying their basic statistics

```python
import asyncio

import callofduty
from callofduty import Mode, Platform, Title


async def main():
    client = await callofduty.Login("YourEmail@email.com", "YourPassword")

    results = await client.SearchPlayers(Platform.Activision, "Captain Price", limit=3)
    for player in results:
        print(f"{player.username} ({player.platform})")

    me = results[1]
    profile = await me.profile(Title.ModernWarfare, Mode.Multiplayer)
    level = profile["level"]
    kd = profile["lifetime"]["all"]["properties"]["kdRatio"]
    wl = profile["lifetime"]["all"]["properties"]["wlRatio"]

    print(f"\n{me.username} ({me.platform})")
    print(f"Level: {level}, K/D Ratio: {kd}, W/L Ratio: {wl}")

    await client.Logout()

asyncio.run(main())
```

