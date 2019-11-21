from .enums import Platform


class User:
    def __init__(self, http, data):
        self.http = http
        self.platform = Platform(data['platform'])
        self.username = data['username']
        self.accountId = data['accountId']
        self.avatar = data['avatar']


    async def profile(self):
        return await self.http.GetProfile(self.platform.value, self.username)

