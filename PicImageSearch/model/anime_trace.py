from typing import Any, NamedTuple

from typing_extensions import override

from .base import BaseSearchItem, BaseSearchResponse


class Character(NamedTuple):
    """Represents a character identified in AnimeTrace search results.

    Contains information about the character's name and the work they appear in.

    Attributes:
        name (str): The name of the character.
        work (str): The title of the work the character appears in.
    """

    name: str
    work: str


class AnimeTraceItem(BaseSearchItem):
    """Represents a single AnimeTrace search result item.

    This class processes and structures individual search results from AnimeTrace,
    providing easy access to various metadata about the found character.

    Attributes:
        origin (dict): The raw JSON data of the search result.
        box (list[float]): Bounding box coordinates of the detected character [x1, y1, x2, y2].
        box_id (str): Unique identifier for the detected box.
        characters (list[Character]): List of possible character matches with their source works.
    """

    def __init__(self, data: dict[str, Any], **kwargs: Any):
        """Initializes an AnimeTraceItem with data from a search result.

        Args:
            data (dict[str, Any]): A dictionary containing the search result data.
            **kwargs (Any): Additional keyword arguments passed to the parent class.
        """
        super().__init__(data, **kwargs)

    @override
    def _parse_data(self, data: dict[str, Any], **kwargs: Any) -> None:
        """Parse search result data.

        Args:
            data (dict[str, Any]): The data to parse.
            **kwargs (Any): Additional keyword arguments (unused).
        """
        self.box: list[float] = data["box"]
        self.box_id: str = data["box_id"]

        # Parse character data
        character_data = data["character"]
        self.characters: list[Character] = []

        for char_info in character_data:
            character = Character(char_info["character"], char_info["work"])
            self.characters.append(character)


class AnimeTraceResponse(BaseSearchResponse[AnimeTraceItem]):
    """Encapsulates a complete AnimeTrace API response.

    This class processes and structures the full response from an AnimeTrace search,
    including all detected characters and their information.

    Attributes:
        raw (list[AnimeTraceItem]): List of processed search result items.
        origin (dict[str, Any]): The raw JSON response data.
        code (int): API response code (0 for success).
        ai (bool): Whether the result was generated by AI.
        trace_id (str): Unique identifier for the trace request.
    """

    def __init__(self, resp_data: dict[str, Any], resp_url: str, **kwargs: Any) -> None:
        """Initializes with the response data.

        Args:
            resp_data (dict[str, Any]): A dictionary containing the parsed response data from AnimeTrace.
            resp_url (str): URL to the search result page.
            **kwargs (Any): Additional keyword arguments passed to the parent class.
        """
        super().__init__(resp_data, resp_url, **kwargs)

    @override
    def _parse_response(self, resp_data: dict[str, Any], **kwargs: Any) -> None:
        """Parse search response data.

        Args:
            resp_data (dict[str, Any]): The response data to parse.
            **kwargs (Any): Additional keyword arguments.
        """
        self.code: int = resp_data["code"]
        self.ai: bool = resp_data.get("ai", False)
        self.trace_id: str = resp_data["trace_id"]

        # Process results
        results = resp_data["data"]
        self.raw: list[AnimeTraceItem] = [AnimeTraceItem(item) for item in results]
