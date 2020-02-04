import logging
from datetime import datetime
from typing import List, Optional

from .enums import Reaction, Title
from .match import Match
from .object import Object
from .player import Player
from .utils import StripHTML

log: logging.Logger = logging.getLogger(__name__)


class FeedItem(Object):
    """
    Represents a Call of Duty feed item object.

    Parameters
    ----------
    player : callofduty.Player
        Player object of the feed item.
    title : callofduty.Title
        Title of the feed item.
    match : callofduty.Match, optional
        Match object of the feed item.
    category : str
        Category of the feed item.
    date : datetime
        Creation date and time of the feed item.
    html : str
        Body of the feed item formatted in HTML.
    text : str
        Body of the feed item.
    favorited : bool
        Boolean value indicating whether the feed item is favorited.
    """

    _type: str = "FeedItem"

    def __init__(self, client, data: dict):
        super().__init__(client)

        self.player: Player = Player(
            self, {"platform": data.pop("platform"), "username": data.pop("username")}
        )
        self.title: Title = Title(data.pop("title"))
        self.match: Optional[Match] = None
        self.category: str = data.pop("category")
        self.date: datetime = datetime.fromtimestamp((data.pop("date") / 1000))
        self.html: str = data.pop("rendered")
        self.text: str = StripHTML(self.html)
        self.favorited: bool = data.pop("favorited")

        if (_matchId := data["meta"].get("matchId")) is not None:
            self.match: Optional[Match] = Match(
                client,
                {"id": _matchId, "platform": self.player.platform, "title": self.title},
            )

    async def react(self, reaction: Reaction) -> None:
        """
        Set a Reaction to the Call of Duty Friend Feed item.

        Parameters
        ----------
        reaction : callofduty.Reaction
            Reaction to add to the feed item.

        Returns
        -------
        None
        """

        await self._client.SetFeedReaction(
            reaction,
            self.player.platform,
            self.player.username,
            self.title,
            (self.date.timestamp() * 1000),
            self.category,
        )

    async def unreact(self) -> None:
        """
        Unset the Reaction to the Call of Duty Friend Feed item.

        Returns
        -------
        None
        """

        await self._client.RemoveFeedReaction(
            self.player.platform,
            self.player.username,
            self.title,
            (self.date.timestamp() * 1000),
            self.category,
        )

    async def favorite(self) -> None:
        """
        Set the Call of Duty Friend Feed item as a favorite.

        Returns
        -------
        None
        """

        await self._client.SetFeedFavorite(
            self.player.platform,
            self.player.username,
            self.title,
            (self.date.timestamp() * 1000),
            self.category,
        )

    async def unfavorite(self) -> None:
        """
        Unset the Call of Duty Friend Feed item as a favorite.

        Returns
        -------
        None
        """

        await self._client.RemoveFeedFavorite(
            self.player.platform,
            self.player.username,
            self.title,
            (self.date.timestamp() * 1000),
            self.category,
        )


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
