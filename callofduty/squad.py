import logging
from typing import List

from .object import Object
from .player import Player

log = logging.getLogger(__name__)


class Squad(Object):
    """
    Represents a Call of Duty Squad object.

    Parameters
    ----------
    name : str
        Name of Squad.
    description : str, optional
        Description of Squad (default is None.)
    avatarUrl : str, optional
        Avatar URL of Squad (default is None.)
    created : str, optional
        Date of Squad creation (default is None.)
    new : bool, optional
        Boolean indication of whether or not the Squad was recently created (default is False.)
    private : bool, optional
        Boolean indication of whether or not the Squad is private (default is False.)
    points : int, optional
        Number of points which the Squad currently has (default is None.)
    owner : object, optional
        Player object representing the Squad owner (default is None.)
    members : list, optional
        Array of player objects representing the Squad members (default is an empty list.)
    """

    _type: str = "squad"

    def __init__(self, client: object, data: dict):
        super().__init__(client)

        self.name: str = data.pop("name")
        self.description: str = data.pop("description", None)
        self.avatarUrl: str = data.pop("avatarUrl", None)
        self.created: str = data.pop("created", None)
        self.new: bool = data.pop("newlyFormed", False)
        self.private: bool = data.pop("private", False)
        self.points: int = data.pop("points", None)

        # The Squads endpoints do not follow the same structure as the rest,
        # so the following is a hacky solution to that problem...
        self.owner = Player(
            client,
            {
                "platform": data["creator"]["platform"],
                "username": data["creator"]["gamerTag"],
                "accountId": data["creator"]["platformId"],
                "avatarUrl": data["creator"]["avatarUrl"],
            },
        )

        self.members: List[Player] = []
        for member in data["members"]:
            self.members.append(
                Player(
                    client,
                    {
                        "platform": member["platform"],
                        "username": member["gamerTag"],
                        "accountId": member["platformId"],
                        "avatarUrl": member["avatarUrl"],
                    },
                )
            )

    async def join(self):
        """Join the Call of Duty Squad."""

        await self._client.JoinSquad(self.name)
