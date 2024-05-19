from typing import Any, Optional


class TraceMoeMe:
    """Encapsulates user-related data from the TraceMoe API.

    Attributes:
        id: User identification, either visitor's IP or user's email.
        priority: Priority level for the user's requests.
        concurrency: Maximum number of simultaneous search requests.
        quota: Total number of searches allowed in the current month.
        quotaUsed: Number of searches already performed in the current month.
    """

    def __init__(self, data: dict[str, Any]):
        """Initializes a TraceMoeMe with user-related data from TraceMoe response.

        Args:
            data: A dictionary containing user-related data from TraceMoe.
        """
        self.id: str = data["id"]
        self.priority: int = data["priority"]
        self.concurrency: int = data["concurrency"]
        self.quota: int = data["quota"]
        self.quotaUsed: int = data["quotaUsed"]


class TraceMoeItem:
    """Represents a single TraceMoe search result item.

    Holds details of a result from a TraceMoe reverse image search.

    Attributes:
        origin: The raw data of the search result item.
        anime_info: Detailed anime information related to the result.
        idMal: MyAnimeList ID of the matched anime.
        title: Various localizations of the anime's title.
        title_native: Native language title of the anime.
        title_english: English title of the anime.
        title_romaji: Romaji title of the anime.
        title_chinese: Chinese title of the anime.
        anilist: Anilist ID of the matched anime.
        synonyms: Alternative English titles for the anime.
        isAdult: Indicates if the anime is adult-themed.
        type: Type of the anime (e.g., "TV", "Movie").
        format: Format of the anime content (e.g., "TV", "Movie", "OVA").
        start_date: Start date of the anime in various formats.
        end_date: End date of the anime in various formats.
        cover_image: Image URL of the anime's cover.
        filename: Filename of the matching anime excerpt.
        episode: Episode number of the matching excerpt.
        From: Start time of the matched excerpt in the anime episode.
        To: End time of the matched excerpt in the anime episode.
        similarity: Similarity percentage between the search image and the matched excerpt.
        video: Video URL of the excerpt.
        image: Thumbnail image URL of the matched scene.
    """

    def __init__(
        self,
        data: dict[str, Any],
        mute: bool = False,
        size: Optional[str] = None,
    ):
        """Initializes a TraceMoeItem with data from a search result.

        Args:
            data: A dictionary containing parsed response data for an individual result.
            mute: Indicates whether to mute the video excerpt.
            size: Size parameter for modifying video and image URLs.
        """
        self.origin: dict[str, Any] = data
        self.anime_info: dict[str, Any] = {}
        self.idMal: int = 0
        self.title: dict[str, str] = {}
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
        if size in ["l", "s", "m"]:
            self.video += f"&size={size}"
            self.image += f"&size={size}"
        # If muted, add mute parameter to video URL
        if mute:
            self.video += "&mute"


class TraceMoeResponse:
    """Encapsulates a TraceMoe reverse image search response.

    Contains the complete response from a TraceMoe reverse image search operation.

    Attributes:
        origin: The raw response data.
        raw: List of TraceMoeItem instances for each search result.
        frameCount: Total number of frames searched in the query.
        error: Error message, if any, from the TraceMoe API.
    """

    def __init__(
        self,
        data: dict[str, Any],
        mute: bool,
        size: Optional[str],
    ):
        """Initializes with the response data.

        Args:
            data: A dictionary containing parsed response data from TraceMoe.
            mute: Flag for muting video excerpts in search results.
            size: Size parameter for modifying video and image URLs.
        """
        self.origin: dict[str, Any] = data
        self.raw: list[TraceMoeItem] = []
        res_docs = data["result"]
        self.raw.extend(
            [
                TraceMoeItem(
                    i,
                    mute=mute,
                    size=size,
                )
                for i in res_docs
            ]
        )
        self.frameCount: int = data["frameCount"]
        self.error: str = data["error"]
