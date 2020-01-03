import logging

from .enums import Language, Platform, Title
from .object import Object

log = logging.getLogger(__name__)


class Season(Object):
    """
    Represents a Call of Duty season object.

    Parameters
    ----------
    title : callofduty.Title
        Call of Duty title which the loot season originates.
    season : int
        Loot season number relative to title.
    platform : callofduty.Platform, optional
        Platform which the loot season is available on (default is PlayStation.)
    name : str, optional
        Official title of Season (default is None.)
    tiers : dict, optional
        JSON data containing tier loot for the Season (default is None.)
    chase : dict, optional
        JSON data containing chase loot for the Season (default is None.)
    language : callofduty.Language, optional
        Language which the loot data should be in (default is English.)
    """

    _type = "season"

    def __init__(self, client: object, data: dict):
        super().__init__(client)

        self.title = Title(data.pop("title"))
        self.season = data.pop("season")
        self.platform = Platform(data.pop("platform"))
        self.name = data.pop("categoryTitle")
        self.tiers = data.pop("tiers")
        self.chase = data.pop("chase")
        self.language = Language(data.pop("language"))
