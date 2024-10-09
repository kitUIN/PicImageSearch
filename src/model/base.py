from abc import ABC, abstractmethod
from typing import Any


class BaseSearchItem(ABC):
    """Base search result item class."""

    def __init__(self, data: Any, **kwargs: Any):
        self.origin: Any = data
        self.url: str = ""
        self.thumbnail: str = ""
        self.title: str = ""
        self.similarity: float = 0.0
        self._parse_data(data, **kwargs)

    @abstractmethod
    def _parse_data(self, data: Any, **kwargs: Any) -> None:
        """Parse search result data."""
        pass


class BaseSearchResponse(ABC):
    """Base search response class."""

    def __init__(self, resp_data: Any, resp_url: str, **kwargs: Any):
        self.origin: Any = resp_data
        self.url: str = resp_url
        self.raw: list[BaseSearchItem] = []
        self._parse_response(resp_data, resp_url=resp_url, **kwargs)

    @abstractmethod
    def _parse_response(self, resp_data: Any, **kwargs: Any) -> None:
        """Parse search response data."""
        pass
