import logging

from .enums import Language, Mode, Platform, Title
from .errors import InvalidLanguage, InvalidMode, InvalidPlatform, InvalidTitle

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
