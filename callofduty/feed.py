import logging
from typing import List

from .object import Object

log: logging.Logger = logging.getLogger(__name__)


class Video(Object):
    """
    Represents a Call of Duty video object.

    Parameters
    ----------
    title : str
        Title of the video.
    description : str
        Description of the video.
    url : str
        YouTube URL of the video.
    length : str
        Length of the video.
    thumbnail : str
        Image URL of the video thumbnail.
    categories : list
        Array of strings containing the video categories.
    """

    _type: str = "Video"

    def __init__(self, client, data: dict):
        super().__init__(client)

        self.title: str = data.pop("title")
        self.description: str = data.pop("description")
        self.url: str = "https://youtu.be/" + data.pop("youtubeId")
        self.length: str = data.pop("length")
        self.thumbnail: str = data.pop("image")
        self.categories: List[str] = data.pop("categories")
