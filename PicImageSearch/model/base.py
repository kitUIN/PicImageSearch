from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

T = TypeVar("T")


class BaseSearchItem(ABC):
    """Base class for search result items.

    This class serves as a template for individual search results from various search engines.
    Each search engine should implement its own subclass with specific parsing logic.

    Attributes:
        origin (Any): The raw data from the search engine.
        url (str): The URL of the found image or page.
        thumbnail (str): The URL of the thumbnail image.
        title (str): The title or description of the search result.
        similarity (float): A float value indicating the similarity score (0.0 to 100.0).
    """

    def __init__(self, data: Any, **kwargs: Any):
        """Initialize a search result item.

        Args:
            data (Any): Raw data from the search engine response.
            **kwargs (Any): Additional keyword arguments for specific search engines.
        """
        self.origin: Any = data
        self.url: str = ""
        self.thumbnail: str = ""
        self.title: str = ""
        self.similarity: float = 0.0
        self._parse_data(data, **kwargs)

    @abstractmethod
    def _parse_data(self, data: Any, **kwargs: Any) -> None:
        """Parse the raw search result data.

        This method should be implemented by subclasses to extract relevant information
        from the raw data and populate the instance attributes.

        Args:
            data (Any): Raw data from the search engine response.
            **kwargs (Any): Additional keyword arguments for specific search engines.
        """
        pass


class BaseSearchResponse(ABC, Generic[T]):
    """Base class for search response handling.

    This class serves as a template for processing and storing search results
    from various search engines.

    Attributes:
        origin (Any): The original response data from the search engine.
        url (str): The URL of the search request.
        raw (list[BaseSearchItem]): A list of BaseSearchItem objects representing individual search results.
    """

    def __init__(self, resp_data: Any, resp_url: str, **kwargs: Any):
        """Initialize a search response.

        Args:
            resp_data (Any): Raw response data from the search engine.
            resp_url (str): The URL of the search request.
            **kwargs (Any): Additional keyword arguments for specific search engines.
        """
        self.origin: Any = resp_data
        self.url: str = resp_url
        self.raw: list[T] = []
        self._parse_response(resp_data, resp_url=resp_url, **kwargs)

    @abstractmethod
    def _parse_response(self, resp_data: Any, **kwargs: Any) -> None:
        """Parse the raw search response data.

        This method should be implemented by subclasses to process the response data
        and populate the raw results list.

        Args:
            resp_data (Any): Raw response data from the search engine.
            **kwargs (Any): Additional keyword arguments for specific search engines.
        """
        pass
