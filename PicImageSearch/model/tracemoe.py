from typing import Any, Optional

from typing_extensions import override

from .base import BaseSearchItem, BaseSearchResponse


class TraceMoeMe:
    """Represents user account information from the TraceMoe API.

    This class encapsulates user-specific data including quotas, priorities, and usage statistics
    returned by the TraceMoe API.

    Attributes:
        id (str): User identifier (IP address for visitors or email for registered users).
        priority (int): User's priority level for request processing.
        concurrency (int): Maximum number of concurrent search requests allowed.
        quota (int): Total search quota allocated for the current month.
        quotaUsed (int): Number of searches consumed in the current month.
    """

    def __init__(self, data: dict[str, Any]):
        """Initializes a TraceMoeMe with user-related data from TraceMoe response.

        Args:
            data (dict[str, Any]): A dictionary containing user-related data from TraceMoe.
        """
        self.id: str = data["id"]
        self.priority: int = data["priority"]
        self.concurrency: int = data["concurrency"]
        self.quota: int = data["quota"]
        self.quotaUsed: int = data["quotaUsed"]


class TraceMoeItem(BaseSearchItem):
    """Represents a single search result from the TraceMoe API.

    This class contains detailed information about a matched anime scene, including
    metadata about the anime and specific timing information for the matched scene.

    Attributes:
        origin (dict): Raw response data from the API.
        anime_info (dict): Comprehensive anime metadata.
        idMal (int): MyAnimeList database ID.
        title_native (str): Title in the original language.
        title_english (str): English title.
        title_romaji (str): Romanized title.
        title_chinese (str): Chinese title.
        anilist (int): AniList database ID.
        synonyms (list[str]): Alternative titles.
        isAdult (bool): Whether the content is adult-oriented.
        type (str): Media type classification.
        format (str): Content format (TV, Movie, OVA, etc.).
        start_date (dict): Anime start date information.
        end_date (dict): Anime end date information.
        cover_image (str): URL to the anime cover image.
        filename (str): Name of the file containing the matched scene.
        episode (int): Episode number of the match.
        From (float): Start timestamp of the matched scene.
        To (float): End timestamp of the matched scene.
        similarity (float): Match confidence percentage (0-100).
        video (str): URL to the preview video of the matched scene.
        image (str): URL to the preview image of the matched scene.
    """

    def __init__(
        self,
        data: dict[str, Any],
        mute: bool = False,
        size: Optional[str] = None,
    ):
        """Initializes a TraceMoeItem with data from a search result.

        Args:
            data (dict[str, Any]): A dictionary containing parsed response data for an individual result.
            mute (bool): Indicates whether to mute the video excerpt.
            size (Optional[str]): Size parameter for modifying video and image URLs.
        """
        super().__init__(data, mute=mute, size=size)

    @override
    def _parse_data(self, data: dict[str, Any], **kwargs: Any) -> None:
        """Parses raw API response data into structured attributes.

        Processes the raw JSON response and initializes all class attributes.
        Handles URL modifications for video and image previews based on size and mute preferences.

        Args:
            data (dict[str, Any]): Raw response dictionary from the TraceMoe API.
            **kwargs (Any): Additional parameters including:
                - size (str): Preview size modifier ('l', 'm', 's')
                - mute (bool): Whether to mute video previews

        Note:
            - Size parameter affects both video and image preview URLs
            - Mute parameter only affects video preview URLs
        """
        self.anime_info: dict[str, Any] = {}
        self.idMal: int = 0
        self.title_native: str = ""
        self.title_english: str = ""
        self.title_romaji: str = ""
        self.title_chinese: str = ""
        self.anilist: int = data["anilist"]
        self.synonyms: list[str] = []
        self.isAdult: bool = False
        self.type: str = ""
        self.format: str = ""
        self.start_date: dict[str, Any] = {}
        self.end_date: dict[str, Any] = {}
        self.cover_image: str = ""
        self.filename: str = data["filename"]
        self.episode: int = data["episode"]
        self.From: float = data["from"]
        self.To: float = data["to"]
        self.similarity: float = float(f"{data['similarity'] * 100:.2f}")
        self.video: str = data["video"]
        self.image: str = data["image"]
        # Modify video and image URLs based on size
        size = kwargs.get("size")
        if size in ["l", "s", "m"]:
            self.video += f"&size={size}"
            self.image += f"&size={size}"
        # If muted, add mute parameter to video URL
        if kwargs.get("mute"):
            self.video += "&mute"


class TraceMoeResponse(BaseSearchResponse[TraceMoeItem]):
    """Represents the complete response from a TraceMoe search operation.

    Encapsulates the entire search response including all matched scenes and metadata
    about the search operation itself.

    Attributes:
        origin (dict): Raw API response data.
        raw (list[TraceMoeItem]): List of processed search results.
        frameCount (int): Total number of frames analyzed during search.
        error (str): Error message if the search encountered issues.
        url (str): URL to the search results page.
    """

    def __init__(
        self,
        resp_data: dict[str, Any],
        resp_url: str,
        mute: bool,
        size: Optional[str],
    ):
        """Initializes with the response data.

        Args:
            resp_data (dict[str, Any]): A dictionary containing parsed response data from TraceMoe.
            resp_url (str): URL to the search result page.
            mute (bool): Flag for muting video excerpts in search results.
            size (Optional[str]): Size parameter for modifying video and image URLs.
        """
        super().__init__(resp_data, resp_url, mute=mute, size=size)

    @override
    def _parse_response(self, resp_data: dict[str, Any], **kwargs: Any) -> None:
        """Processes the raw API response into structured data.

        Converts raw JSON response into TraceMoeItem instances and extracts
        metadata about the search operation.

        Args:
            resp_data (dict[str, Any]): Raw response dictionary from the TraceMoe API.
            **kwargs (Any): Additional parameters including:
                - mute (bool): Whether to mute video previews
                - size (str): Preview size modifier

        Note:
            The parsed results are stored in the `raw` attribute as TraceMoeItem instances.
        """
        res_docs = resp_data["result"]
        self.raw.extend(
            [
                TraceMoeItem(
                    i,
                    mute=kwargs.get("mute", False),
                    size=kwargs.get("size"),
                )
                for i in res_docs
            ]
        )
        self.frameCount: int = resp_data["frameCount"]
        self.error: str = resp_data["error"]
