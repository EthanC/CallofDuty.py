import logging

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
        Description of Squad.
    avatarUrl : str, optional
        Avatar URL of Squad.
    created : str, optional
        Date of Squad creation.
    new : bool, optional
        Boolean indication of whether or not the Squad was recently created.
    private : bool, optional
        Boolean indication of whether or not the Squad is private.
    points : int, optional
        Number of points which the Squad currently has.
    owner : object, optional
        Player object representing the Squad owner.
    members : list, optional
        Array of player objects representing the Squad members.
    """

    _type = "squad"

    def __init__(self, client: object, data: dict):
        super().__init__(client, data)

        self.name = data.pop("name")
        self.description = data.pop("description", None)
        self.avatarUrl = data.pop("avatarUrl", None)
        self.created = data.pop("created", None)
        self.new = data.pop("newlyFormed", None)
        self.private = data.pop("private", None)
        self.points = data.pop("points", None)

        # The Squads endpoints do not follow the same structure as the rest,
        # so the following is a hacky solution to that problem...
        self.owner = Player(
            client,
            {
                "platform": data["creator"]["platform"],
                "username": data["creator"]["gamerTag"],
                "accountId": data["creator"]["platformId"],
                "avatarUrls": [data["creator"]["avatarUrl"]],
            },
        )

        _members = []
        for member in data["members"]:
            _members.append(
                Player(
                    client,
                    {
                        "platform": member["platform"],
                        "username": member["gamerTag"],
                        "accountId": member["platformId"],
                        "avatarUrls": [member["avatarUrl"]],
                    },
                )
            )
        self.members = _members
