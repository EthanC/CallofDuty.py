from enum import Enum


class Platform(Enum):
    Activision = "uno"
    PlayStation = "psn"
    Xbox = "xbl"
    Steam = "steam"
    BattleNet = "battle"


class Title(Enum):
    ModernWarfare = "mw"
    BlackOps4 = "bo4"
    WWII = "wwii"
    InfiniteWarfare = "iw"
    BlackOps3 = "bo3"


class Mode(Enum):
    Multiplayer = "mp"
    Zombies = "zm"
    Blackout = "wz"
