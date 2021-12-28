<div align="center">

![CallofDuty.py](https://i.imgur.com/HXy6Dkd.png)

<a href="https://pypi.python.org/pypi/callofduty.py"><img src="https://img.shields.io/pypi/v/callofduty.py?label=Version&style=for-the-badge" /></a>
<a href="https://pypi.python.org/pypi/callofduty.py"><img src="https://img.shields.io/pypi/dm/callofduty.py?style=for-the-badge" /></a>
<a href="https://twitter.com/Mxtive"><img src="https://img.shields.io/twitter/follow/Mxtive?color=1da1f2&label=Twitter&style=for-the-badge" /></a>
<a href="https://discord.gg/callofduty"><img src="https://img.shields.io/discord/136986169563938816?color=7289DA&label=Discord&style=for-the-badge" /></a>

</div>

# CallofDuty.py

CallofDuty.py is an asynchronous, object-oriented Python wrapper for the Call of Duty API.

## Features

-   Asynchronous and Pythonic using `async` and `await`
-   Type checks and editor completion using [Type Hints](https://www.python.org/dev/peps/pep-0484/)
-   Object-oriented and predictable abstractions

## Usage

Construct a new Call of Duty client, then use the various services on the client to access different parts of the Call of Duty API.

### Installation

CallofDuty.py requires Python 3.10 or greater. Once this requirement is met, simply install CallofDuty.py!

```
pip install callofduty.py

# or

poetry add callofduty.py
```

### Example

The following is a complete example which demonstrates:

-   Authenticating with the Call of Duty API
-   Searching for a user
-   Listing the first 3 search results
-   Getting the Modern Warfare Multiplayer profile of the second result
-   Displaying their basic statistics

```py
import asyncio

import callofduty
from callofduty import Mode, Platform, Title


async def main():
    client = await callofduty.Login("YourEmail@email.com", "YourPassword")

    results = await client.SearchPlayers(Platform.Activision, "Captain Price", limit=3)
    for player in results:
        print(f"{player.username} ({player.platform.name})")

    me = results[1]
    profile = await me.profile(Title.ModernWarfare, Mode.Multiplayer)

    level = profile["level"]
    kd = profile["lifetime"]["all"]["properties"]["kdRatio"]
    wl = profile["lifetime"]["all"]["properties"]["wlRatio"]

    print(f"\n{me.username} ({me.platform.name})")
    print(f"Level: {level}, K/D Ratio: {kd}, W/L Ratio: {wl}")

asyncio.get_event_loop().run_until_complete(main())
```

## Releases

CallofDuty.py follows [Semantic Versioning](https://semver.org/) for tagging releases of the project.

Changelogs can be found on the [Releases](https://github.com/EthanC/CallofDuty.py/releases) page and follow the [Keep a Changelog](https://keepachangelog.com/) format.

## Contributing

The goal is to cover the entirety of the Call of Duty API, so contributions are always welcome. The calling pattern is pretty well-established, so adding new methods is relatively straightforward. See [`CONTRIBUTING.md`](https://github.com/EthanC/CallofDuty.py/blob/master/.github/CONTRIBUTING.md) for details.

## Thanks & Credits

-   [Tustin](https://github.com/Tustin) - Call of Duty API Authorization Flow
-   [Activision](https://www.activision.com/) - Call of Duty Logo & API Service
