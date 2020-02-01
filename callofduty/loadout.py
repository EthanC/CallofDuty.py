import logging
from typing import List, Optional

from .object import Object

log: logging.Logger = logging.getLogger(__name__)


class Loadout(Object):
    """
    Represents a Call of Duty loadout object.

    Parameters
    ----------
    name : str
        Name of the loadout.
    primary : callofduty.LoadoutWeapon
        Primary weapon slot of the loadout.
    secondary : callofduty.LoadoutWeapon
        Secondary weapon slot of the loadout.
    equipment : list
        Array of LoadoutItem objects of the loadout's equipment.
    perks : list
        Array of LoadoutItem objects of the loadout's perks.
    wildcards : list
        Array of LoadoutItem objects of the loadout's wildcards.
    unlocked : bool
        Boolean value indicating whether the loadout slot is unlocked.
    """

    _type: str = "Loadout"

    def __init__(self, client, data: dict):
        super().__init__(client)

        self.name: str = data.pop("customClassName")
        self.primary: LoadoutWeapon = LoadoutWeapon(self, data.pop("primaryWeapon"))
        self.secondary: LoadoutWeapon = LoadoutWeapon(self, data.pop("secondaryWeapon"))
        self.equipment: List[LoadoutItem] = []
        self.perks: List[LoadoutItem] = []
        self.wildcards: List[LoadoutItem] = []
        self.unlocked: bool = data.pop("unlocked")

        if (_equipment := data.pop("equipment")) is not None:
            self.equipment.append(LoadoutItem(self, _equipment))

        if (_gear := data.pop("gear")) is not None:
            self.equipment.append(LoadoutItem(self, _gear))

        for _perk in data.pop("perks"):
            self.perks.append(LoadoutItem(self, _perk))

        for _wildcard in data.pop("wildcards"):
            self.wildcards.append(LoadoutItem(self, _wildcard))


class LoadoutWeapon(Object):
    """
    Represents a Call of Duty loadout weapon object.

    Parameters
    ----------
    id : str
        ID of the weapon.
    variant : str, optional
        ID of the weapon variant (default is None.)
    attachments : list
        Array of LoadoutItem objects for the weapon's attachments.
    camo : bool
        Boolean value indicating whether a camo is equipped to the weapon.
    """

    _type: str = "LoadoutWeapon"

    def __init__(self, client, data: dict):
        super().__init__(client)

        self.id: str = data.pop("id")
        self.variant: Optional[str] = None
        self.attachments: List[LoadoutItem] = []
        self.camo: bool = data.pop("camoEquipped")

        if (_variant := data.pop("variant")) is not None:
            self.variant: Optional[str] = _variant["id"]

        # Optics and Operator Mods are attachments, there's no reason to
        # seperate them from the attachments array.
        # This is also to (hopefully) make Modern Warfare support easier.
        if (_optic := data.pop("optic")) is not None:
            self.attachments.append(LoadoutItem(self, _optic))

        if (_opMod := data.pop("operatorMod")) is not None:
            self.attachments.append(LoadoutItem(self, _opMod))

        if (_attachments := data.pop("attachments")) is not None:
            for _attachment in _attachments:
                self.attachments.append(LoadoutItem(self, _attachment))


class LoadoutItem(Object):
    """
    Represents a Call of Duty loadout item object.

    Parameters
    ----------
    id : str
        ID of the item.
    """

    _type: str = "LoadoutItem"

    def __init__(self, client, data: dict):
        super().__init__(client)

        self.id: str = data.pop("id")
