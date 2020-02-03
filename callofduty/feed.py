import logging
from datetime import datetime
from typing import List, Optional

from .object import Object
from .utils import StripHTML

log: logging.Logger = logging.getLogger(__name__)


class Blog(Object):
    """
    Represents a Call of Duty blog object.

    Parameters
    ----------
    author : str, optional
        Author of the blog post.
    title : str
        Title of the blog post.
    subtitle : str, optional
        Subtitle of the blog post.
    html : str, optional
        Body of the blog post formatted in HTML.
    text : str, optional
        Body of the blog post.
    url : str
        URL of the blog post.
    thumbnail : str
        Image URL of the blog post thumbnail.
    category : str
        Category of the blog post.
    published : datetime
        Publish date and time of the blog post.
    """

    _type: str = "Blog"

    def __init__(self, client, data: dict):
        super().__init__(client)

        self.author: Optional[str] = data.pop("author", None)
        self.title: str = data.pop("title")
        self.subtitle: Optional[str] = data.pop("subTitle", None)
        self.html: Optional[str] = data.pop("html", None)
        self.text: Optional[str] = StripHTML(
            self.html
        ) if self.html is not None else None
        self.url: str = data.pop("url")
        self.thumbnail: str = data.pop("dimg")
        self.category: str = data["metadata"].pop("contentItemType")
        self.published: datetime = datetime(
            data["publishedDate"].pop("year"),
            data["publishedDate"].pop("month"),
            data["publishedDate"].pop("dayOfMonth"),
            data["publishedDate"].pop("hourOfDay"),
            data["publishedDate"].pop("minute"),
            data["publishedDate"].pop("second"),
        )


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
