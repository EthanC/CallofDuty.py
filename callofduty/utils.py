import logging

from .enums import GameMode, GameType, Language, Mode, Platform, TimeFrame, Title
from .errors import (
    InvalidGameMode,
    InvalidGameType,
    InvalidLanguage,
    InvalidMode,
    InvalidPlatform,
    InvalidTimeFrame,
    InvalidTitle,
)

log = logging.getLogger(__name__)


def VerifyPlatform(value: Platform):
    """
    Raise an InvalidPlatform client exception if a value which is not
    present in the Platform enum is passed.

    Parameters
    ----------
    value : callofduty.Platform
        Value to confirm is present in the Platform enum.
    """

    if value not in Platform:
        raise InvalidPlatform(f"{value} is not a valid platform")


def VerifyTitle(value: Title):
    """
    Raise an InvalidTitle client exception if a value which is not
    present in the Title enum is passed.

    Parameters
    ----------
    value : callofduty.Title
        Value to confirm is present in the Title enum.
    """

    if value not in Title:
        raise InvalidTitle(f"{value} is not a valid title")


def VerifyMode(value: Mode):
    """
    Raise an InvalidMode client exception if a value which is not
    present in the Mode enum is passed.

    Parameters
    ----------
    value : callofduty.Mode
        Value to confirm is present in the Mode enum.
    """

    # TODO Validate mode for title
    # e.g. Zombies is not a valid mode for Modern Warfare

    if value not in Mode:
        raise InvalidMode(f"{value} is not a valid mode")


def VerifyLanguage(value: Language):
    """
    Raise an InvalidLanguage client exception if a value which is not
    present in the Language enum is passed.

    Parameters
    ----------
    value : callofduty.Language
        Value to confirm is present in the Language enum.
    """

    if value not in Language:
        raise InvalidLanguage(f"{value} is not a valid language")


def VerifyTimeFrame(value: TimeFrame):
    """
    Raise an InvalidTimeFrame client exception if a value which is not
    present in the TimeFrame enum is passed.

    Parameters
    ----------
    value : callofduty.TimeFrame
        Value to confirm is present in the TimeFrame enum.
    """

    if value not in TimeFrame:
        raise InvalidTimeFrame(f"{value} is not a valid time frame")


def VerifyGameType(value: GameType):
    """
    Raise an InvalidGameType client exception if a value which is not
    present in the GameType enum is passed.

    Parameters
    ----------
    value : callofduty.GameType
        Value to confirm is present in the GameType enum.
    """

    if value not in GameType:
        raise InvalidGameType(f"{value} is not a valid game type")


def VerifyGameMode(value: GameMode):
    """
    Raise an InvalidGameMode client exception if a value which is not
    present in the GameMode enum is passed.

    Parameters
    ----------
    value : callofduty.GameMode
        Value to confirm is present in the GameMode enum.
    """

    # TODO Validate game mode for title
    # e.g. Cyber Attack is not a valid mode for Black Ops 4

    if value not in GameMode:
        raise InvalidGameMode(f"{value} is not a valid game mode")
