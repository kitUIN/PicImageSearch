from typing import Any, Callable, Optional

from .base import BaseSearchItem, BaseSearchResponse


class BingItem(BaseSearchItem):
    """Represents a single Bing search result item.

    Holds details of a result from a Bing reverse image search.

    Attributes:
        origin: The raw data of the search result item.
        title: Title of the search result.
        url: URL of the webpage with the image.
        thumbnail: URL of the thumbnail image.
        image_url: URL of the page hosting the image.
    """

    def _parse_data(self, data: dict[str, Any], **kwargs) -> None:
        """Parse search result data."""
        self.title: str = data.get("name", "")
        self.url: str = data.get("hostPageUrl", "")
        self.thumbnail: str = data.get("thumbnailUrl", "")
        self.image_url: str = data.get("contentUrl", "")


class RelatedSearchItem:
    """Represents a related search item suggested by Bing.

    Attributes:
        text: Text of the related search query.
        thumbnail: URL of the thumbnail image associated with the related search.
    """

    def __init__(self, data: dict[str, Any]):
        self.text: str = data.get("text", "")
        self.thumbnail: str = data.get("thumbnail", {}).get("url", "")


class PagesIncludingItem:
    """Represents a page that includes the searched image.

    Attributes:
        name: Title of the page including the image.
        thumbnail: URL of the page's thumbnail.
        url: URL of the page.
        image_url: URL of the image on the page.
    """

    def __init__(self, data: dict[str, Any]):
        self.name: str = data.get("name", "")
        self.thumbnail: str = data.get("thumbnailUrl", "")
        self.url: str = data.get("hostPageUrl", "")
        self.image_url: str = data.get("contentUrl", "")


class VisualSearchItem:
    """Represents a visually similar image found by Bing.

    Attributes:
        name: Title or description of the visually similar image.
        thumbnail: URL of the thumbnail for the visually similar image.
        url: URL of the visually similar image.
        image_url: URL of the page hosting the visually similar image.

    """

    def __init__(self, data: dict[str, Any]):
        self.name: str = data.get("name", "")
        self.thumbnail: str = data.get("thumbnailUrl", "")
        self.url: str = data.get("hostPageUrl", "")
        self.image_url: str = data.get("contentUrl", "")


class Attraction:
    """Represents a travel attraction suggested by Bing.

    Attributes:
        url: URL for information about the attraction.
        title: Name of the attraction.
        search_url: URL for querying again on Bing about the attraction.
        interest_types: List of interest types associated with the attraction.
    """

    def __init__(self, data: dict[str, Any]):
        self.url: str = data.get("attractionUrl", "")
        self.title: str = data.get("title", "")
        self.search_url: str = data.get("requeryUrl", "")
        self.interest_types: list[str] = data.get("interestTypes", [])


class TravelCard:
    """Represents a travel card with information related to the image.

    Attributes:
        card_type: Type of the travel card.
        title: Title of the travel card.
        url: URL associated with the travel card.
        image_url: Image URL on the travel card.
        image_source_url: Source URL of the image on the travel card.
    """

    def __init__(self, data: dict[str, Any]):
        self.card_type: str = data.get("cardType", "")
        self.title: str = data.get("title", "")
        self.url: str = data.get("clickUrl", "")
        self.image_url: str = data.get("image", "")
        self.image_source_url: str = data.get("imageSourceUrl", "")


class TravelInfo:
    """Represents travel-related information extracted by Bing.

    Attributes:
        destination_name: Name of the travel destination.
        travel_guide_url: URL to a travel guide related to the destination.
        attractions: List of Attraction objects representing points of interest.
        travel_cards: List of TravelCard objects with related travel info.
    """

    def __init__(self, data: dict[str, Any]):
        self.destination_name: str = data.get("destinationName", "")
        self.travel_guide_url: str = data.get("travelGuideUrl", "")
        self.attractions: list[Attraction] = [
            Attraction(x) for x in data.get("attractions", [])
        ]
        self.travel_cards: list[TravelCard] = [
            TravelCard(x) for x in data.get("travelCards", [])
        ]


class EntityItem:
    """Represents an entity identified in the image by Bing.

    Attributes:
        name: Name of the entity.
        thumbnail: URL of the entity's thumbnail image.
        description: Description of the entity.
        profiles: List of social media profiles associated with the entity.
        short_description: Short description or entity type hint.
    """

    def __init__(self, data: dict[str, Any]):
        self.name: str = data.get("name", "")
        self.thumbnail: str = data.get("image", {}).get("thumbnailUrl", "")
        self.description: str = data.get("description", "")
        self.profiles: list[dict[str, str]] = []

        if social_media := data.get("socialMediaInfo"):
            self.profiles = [
                {
                    "url": profile.get("profileUrl"),
                    "social_network": profile.get("socialNetwork"),
                }
                for profile in social_media.get("profiles", [])
            ]

        self.short_description: str = data.get("entityPresentationInfo", {}).get(
            "entityTypeDisplayHint", ""
        )


class BingResponse(BaseSearchResponse):
    """Encapsulates a Bing reverse image search response.

    Contains the complete response from a Bing reverse image search operation.

    Attributes:
        origin: The raw response data.
        pages_including: List of PagesIncludingItem objects.
        visual_search: List of VisualSearchItem objects.
        related_searches: List of RelatedSearchItem objects.
        best_guess: Bing's best guess for the image query.
        travel: TravelInfo object if travel-related information is found.
        entities: List of EntityItem objects representing identified entities.
        url: URL to the search results page.
    """

    def _parse_response(self, resp_data: dict[str, Any], **kwargs: Any) -> None:
        """Parse search response data."""
        self.pages_including: list[PagesIncludingItem] = []
        self.visual_search: list[VisualSearchItem] = []
        self.related_searches: list[RelatedSearchItem] = []
        self.best_guess: Optional[str] = None
        self.travel: Optional[TravelInfo] = None
        self.entities: list[EntityItem] = []

        if tags := resp_data.get("tags"):
            for tag in tags:
                for action in tag.get("actions", []):
                    self._parse_action(action)

    def _parse_action(self, action: dict[str, Any]) -> None:
        """Parse a single action from the response data."""
        action_type: str = action.get("actionType", "")
        action_handlers: dict[str, Callable[[dict[str, Any]], None]] = {
            "PagesIncluding": self._handle_pages_including,
            "VisualSearch": self._handle_visual_search,
            "RelatedSearches": self._handle_related_searches,
            "BestRepresentativeQuery": self._handle_best_query,
            "Travel": self._handle_travel,
            "Entity": self._handle_entity,
        }

        if handler := action_handlers.get(action_type):
            handler(action)

    def _handle_pages_including(self, action: dict[str, Any]) -> None:
        if value := action.get("data", {}).get("value"):
            self.pages_including.extend([PagesIncludingItem(val) for val in value])

    def _handle_visual_search(self, action: dict[str, Any]) -> None:
        if value := action.get("data", {}).get("value"):
            self.visual_search.extend([VisualSearchItem(val) for val in value])

    def _handle_related_searches(self, action: dict[str, Any]) -> None:
        if value := action.get("data", {}).get("value"):
            self.related_searches.extend([RelatedSearchItem(val) for val in value])

    def _handle_best_query(self, action: dict[str, Any]) -> None:
        self.best_guess = action.get("displayName")

    def _handle_travel(self, action: dict[str, Any]) -> None:
        self.travel = TravelInfo(action.get("data", {}))

    def _handle_entity(self, action: dict[str, Any]) -> None:
        if data := action.get("data"):
            self.entities.append(EntityItem(data))
