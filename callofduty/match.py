import logging

from .enums import Platform
from .errors import CallofDutyException, InvalidMatchId
from .user import User

log = logging.getLogger(__name__)


class Match:
    def __init__(self, http: object, platform: Platform, match: object):
        self.http = http
        self.platform = platform
        self.match = match

    async def teams(self):
        # TODO (Tustin) Cache me!
        data = await self.http.GetMatch(self.platform.value, self.match["matchID"])

        if data["status"] != "success":
            raise InvalidMatchId(f"No match with ID {self.match['matchID']} found")

        # The API doesn't state which team is axis/allies,
        # so no array key will be used
        teams = []

        for team in data["data"]["teams"]:
            it = []  # Current team iterator

            for player in team:
                it.append(
                    User(
                        self.http,
                        platform=player["provider"],
                        username=player["unoUsername"],
                    )
                )

            teams.append(it)

        return teams
