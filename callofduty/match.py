from .enums import Platform
from .errors import InvalidMatchIdError, CallofDutyException

import callofduty.user

class Match:
    def __init__(self, http: object, platform: Platform, match: object):
        self.http = http
        self.platform = platform
        self.match = match

    async def teams(self):
        # TODO (Tustin) Cache me!
        data = await self.http.GetMatch(self.platform.value, self.match['matchID'])

        if data['status'] != 'success':
            raise InvalidMatchIdError(f"No match with ID {self.match['matchID']} found")

        # The API doesnt state which team is axis/allies so no array key will be used
        self.teams = []

        for team in data['data']['teams']:
            it = [] # current team iterator

            for player in team:
                it.append(callofduty.User(self.http, platform=player['provider'], username=player['unoUsername']))

            self.teams.append(it)
        
        return self.teams

