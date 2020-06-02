import logging
import re

from .enums import GameType, Language, Mode, Platform, Reaction, TimeFrame, Title
from .errors import (
    InvalidGameType,
    InvalidLanguage,
    InvalidMode,
    InvalidPlatform,
    InvalidReaction,
    InvalidTimeFrame,
    InvalidTitle,
)

log: logging.Logger = logging.getLogger(__name__)


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
        raise InvalidPlatform(f"{value.name} is not a valid platform")


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
        raise InvalidTitle(f"{value.name} is not a valid title")


def VerifyMode(value: Mode, title: Title):
    """
    Raise an InvalidMode client exception if a value which is not
    present in the Mode enum is passed.

    Parameters
    ----------
    value : callofduty.Mode
        Value to confirm is present in the Mode enum.
    title : callofduty.Title
        Title to confirm is compatible with the Mode.
    """

    if value not in Mode:
        raise InvalidMode(f"{value.name} is not a valid mode")
    elif (value == Mode.Zombies) and (title == Title.ModernWarfare):
        raise InvalidMode(f"{value.name} is not a valid mode for title {title.name}")
    elif (value == Mode.Warzone) and (title != Title.ModernWarfare):
        raise InvalidMode(f"{value.name} is not a valid mode for title {title.name}")


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
        raise InvalidLanguage(f"{value.name} is not a valid language")


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
        raise InvalidTimeFrame(f"{value.name} is not a valid time frame")


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
        raise InvalidGameType(f"{value.name} is not a valid game type")


def VerifyReaction(value: Reaction):
    """
    Raise an InvalidReaction client exception if a value which is not
    present in the Reaction enum is passed.

    Parameters
    ----------
    value : callofduty.Reaction
        Value to confirm is present in the Reaction enum.
    """

    if value not in Reaction:
        raise InvalidReaction(f"{value.name} is not a valid reaction")


def StripHTML(input: str) -> str:
    """
    Strip the HTML formatting from a string.

    Parameters
    ----------
    input : str
        HTML formatted string.

    Returns
    -------
    str
        Input string without the HTML formatting.
    """

    # Regex is hideous, but this gets the job done faster than an external
    # library. This is also future-proof against any sort of HTML characters,
    # such as &nbsp and &amp.
    expression: re.Pattern[str] = re.compile(
        "<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});"
    )

    return re.sub(expression, "", input)
