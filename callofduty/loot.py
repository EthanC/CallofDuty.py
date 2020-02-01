import logging
from typing import List, Optional

from .enums import Language, Platform, Title
from .object import Object

log: logging.Logger = logging.getLogger(__name__)


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
    tiers : list, optional
        Array of Loot Items containing tier loot for the Season (default is an empty list.)
    chase : list, optional
        Array of Loot Items containing chase loot for the Season (default is an empty list.)
    language : callofduty.Language, optional
        Language which the loot data should be in (default is English.)
    """

    _type: str = "Season"

    def __init__(self, client, data: dict):
        super().__init__(client)

        self.title: Title = Title(data.pop("title"))
        self.season: int = data.pop("season")
        self.platform: Platform = Platform(data.pop("platform"))
        self.name: Optional[str] = data.pop("categoryTitle", None)
        self.tiers: List[LootItem] = []
        self.chase: List[LootItem] = []
        self.language: Language = Language(data.pop("language"))

        for tier in (_tiers := data.pop("tiers", [])) :
            self.tiers.append(LootItem(self, _tiers[tier]))

        for chase in (_chase := data.pop("chase", [])) :
            self.chase.append(LootItem(self, _chase[chase]))


class LootItem(Object):
    """
    Represents a Call of Duty loot item object.

    Parameters
    ----------
    id : str
        Internal name of the loot item.
    name : str
        Name of the loot item.
    category : str
        Type of the loot item.
    rarity : str
        Rarity of the loot item.
    tier : int
        Tier which the loot item is rewarded.
    image : str
        Image URL for the loot item.
    free : bool, optional
        Boolean indicating whether or not the loot item is available for free (default is False.)
    """

    _type: str = "LootItem"

    def __init__(self, client, data: dict):
        super().__init__(client)

        self.id: str = data.pop("name")
        self.name: str = data.pop("label")
        self.category: str = data.pop("type")
        self.rarity: str = data.pop("rarity")
        self.tier: int = int(data.pop("tier"))
        self.image: str = data.pop("image")
        self.free: bool = data.pop("free", False)
