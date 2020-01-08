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

    _type: str = "season"

    def __init__(self, client: object, data: dict):
        super().__init__(client)

        self.title: str = Title(data.pop("title"))
        self.season: int = data.pop("season")
        self.platform: Platform = Platform(data.pop("platform"))
        self.name: str = data.pop("categoryTitle", None)
        self.tiers: dict = data.pop("tiers", None)
        self.chase: dict = data.pop("chase", None)
        self.language: Language = Language(data.pop("language"))
