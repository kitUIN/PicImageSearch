from typing import Any, Dict, List, Optional


class TraceMoeMe:
    """Encapsulates user-related data from the TraceMoe API.

    Attributes:
        id: The identification representing either the visitor's IP address or the user's email address.
        priority: An integer describing the priority level of the user's requests.
        concurrency: The number of concurrent search requests the user is allowed to make.
        quota: The total search quota allocated to the user for the current month.
        quotaUsed: The amount of the search quota that has already been used during the current month.
    """

    def __init__(self, data: Dict[str, Any]):
        """Initializes a TraceMoeMe with user-related data from TraceMoe response.

        Args:
            data: A dictionary containing the user-related data from the TraceMoe response.
        """
        self.id: str = data[
            "id"
        ]  # IP 地址（访客）或电子邮件地址（用户） (IP address (visitor) or email address (user))
        self.priority: int = data["priority"]  # 优先级 (priority)
        self.concurrency: int = data[
            "concurrency"
        ]  # 搜索请求数量 (number of search requests)
        self.quota: int = data["quota"]  # 本月的搜索配额 (search quota for this month)
        self.quotaUsed: int = data[
            "quotaUsed"
        ]  # 本月已经使用的搜索配额 (search quota used this month)


class TraceMoeItem:
    """A single search result from the TraceMoe image search engine.

    Attributes:
        origin: The original response data for the item.
        anime_info: A dictionary with detailed anime information related to the result.
        idMal: The MyAnimeList ID of the matched anime.
        title: A dictionary containing various localizations of the anime's title.
        title_native: The anime's native language title.
        title_english: The anime's English title.
        title_romaji: The anime's Romaji (latinized Japanese) title.
        title_chinese: The anime's Chinese title.
        anilist: The Anilist ID of the matched anime.
        synonyms: A list of alternative English titles for the anime.
        isAdult: A boolean indicating if the anime is adult-themed.
        type: A string indicating the anime's type (e.g. "TV", "Movie").
        format: A string indicating the format of the matched content.
        start_date: A dictionary containing the starting date of the anime.
        end_date: A dictionary containing the ending date of the anime.
        cover_image: The URL to the image of the anime's cover.
        filename: The filename of the matching anime excerpt.
        episode: The episode number of the matching excerpt.
        From: The starting timestamp of the matching excerpt.
        To: The ending timestamp of the matching excerpt.
        similarity: The percentage similarity between the search image and the matched anime excerpt.
        video: The URL to the video excerpt.
        image: The URL to the thumbnail image of the matched scene.
    """

    def __init__(
        self,
        data: Dict[str, Any],
        mute: bool = False,
        size: Optional[str] = None,
    ):
        """Initializes a TraceMoeItem with data parsed from the TraceMoe API response.

        Args:
            data: A dictionary containing the parsed response data for an individual result.
            mute: A flag indicating whether to mute the video excerpt.
            size: An optional size parameter that modifies the video and image URL to return different sizes.
        """
        self.origin: Dict[str, Any] = data  # 原始数据 (raw data)
        self.anime_info: Dict[str, Any] = {}  # 动画信息 (anime info)
        self.idMal: int = (
            0  # 匹配的MyAnimelist ID见https://myanimelist.net/ (matched MyAnimelist ID)
        )
        self.title: Dict[str, str] = {}
        self.title_native: str = ""
        """番剧国际命名"""
        self.title_english: str = ""
        self.title_romaji: str = ""
        self.title_chinese: str = ""
        self.anilist: int = data[
            "anilist"
        ]  # 匹配的Anilist ID见https://anilist.co/ (matched Anilist ID)
        self.synonyms: List[str] = []  # 备用英文标题 (alternative English titles)
        self.isAdult: bool = False
        self.type: str = ""
        self.format: str = ""
        self.start_date: Dict[str, Any] = {}
        self.end_date: Dict[str, Any] = {}
        self.cover_image: str = ""
        self.filename: str = data["filename"]
        self.episode: int = data["episode"]
        self.From: float = data["from"]
        self.To: float = data["to"]
        self.similarity: float = float(f"{data['similarity'] * 100:.2f}")
        self.video: str = data["video"]
        self.image: str = data["image"]
        if size in ["l", "s", "m"]:  # 大小设置 (size setting)
            self.video += f"&size={size}"
            self.image += f"&size={size}"
        if mute:  # 视频静音设置 (video mute setting)
            self.video += "&mute"


class TraceMoeResponse:
    """Encapsulates the overall response from a TraceMoe image search.

    Attributes:
        origin: The original response data received from the TraceMoe API.
        raw: A list of TraceMoeItem instances representing individual search results.
        frameCount: An integer indicating the total number of frames searched.
        error: A string with the error message, if any, from the search.
    """

    def __init__(
        self,
        data: Dict[str, Any],
        mute: bool,
        size: Optional[str],
    ):
        """Initializes a TraceMoeResponse with data parsed from the TraceMoe API response.

        Args:
            data: A dictionary containing the parsed response data from TraceMoe.
            mute: A flag indicating whether to mute the video excerpts in the search results.
            size: An optional size parameter that modifies the video and image URLs in the search results.
        """
        self.origin: Dict[str, Any] = data  # 原始数据 (raw data)
        self.raw: List[TraceMoeItem] = []  # 结果返回值 (result returned from source)
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
        self.frameCount: int = data[
            "frameCount"
        ]  # 搜索的帧总数 (total number of frames searched)
        self.error: str = data["error"]  # 错误报告 (error message)
