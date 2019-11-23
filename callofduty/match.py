import logging

from .enums import Platform, Title
from .errors import CallofDutyException, InvalidMatchId, InvalidTitle
from .user import User

log = logging.getLogger(__name__)


class Match:
    def __init__(self, http: object, title: Title, platform: Platform, match: object):
        self.http = http
        self.title = title
        self.platform = platform
        self.match = match

    async def teams(self):
        matchId = self.match["matchId"]

        # TODO (Tustin) Cache me!
        data = await self.http.GetMatch(self.title.value, self.platform.value, matchId)

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
