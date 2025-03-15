from typing import Any, Callable, Optional

from typing_extensions import override

from .base import BaseSearchItem, BaseSearchResponse


class BingItem(BaseSearchItem):
    """Represents a single Bing search result item.

    Attributes:
        origin (dict): The raw JSON data of the search result item.
        title (str): Title or name of the search result.
        url (str): URL of the webpage containing the image.
        thumbnail (str): URL of the thumbnail version of the image.
        image_url (str): Direct URL to the full-size image.
    """

    def __init__(self, data: dict[str, Any], **kwargs: Any):
        """Initializes a BingItem with data from a search result.

        Args:
            data (dict[str, Any]): A dictionary containing the search result data.
        """
        super().__init__(data, **kwargs)

    @override
    def _parse_data(self, data: dict[str, Any], **kwargs: Any) -> None:
        """Parse search result data."""
        self.title: str = data.get("name", "")
        self.url: str = data.get("hostPageUrl", "")
        self.thumbnail: str = data.get("thumbnailUrl", "")
        self.image_url: str = data.get("contentUrl", "")


class RelatedSearchItem:
    """Represents a related search suggestion from Bing's image search.

    Attributes:
        text (str): The suggested search query text.
        thumbnail (str): URL of the thumbnail image associated with this suggestion.
    """

    def __init__(self, data: dict[str, Any]):
        self.text: str = data.get("text", "")
        self.thumbnail: str = data.get("thumbnail", {}).get("url", "")


class PagesIncludingItem:
    """Represents a webpage that contains the searched image.

    Attributes:
        name (str): Title of the webpage.
        thumbnail (str): URL of the thumbnail image from this page.
        url (str): URL of the webpage containing the image.
        image_url (str): Direct URL to the image on this page.
    """

    def __init__(self, data: dict[str, Any]):
        self.name: str = data.get("name", "")
        self.thumbnail: str = data.get("thumbnailUrl", "")
        self.url: str = data.get("hostPageUrl", "")
        self.image_url: str = data.get("contentUrl", "")


class VisualSearchItem:
    """Represents a visually similar image found by Bing's visual search.

    Attributes:
        name (str): Title or description of the similar image.
        thumbnail (str): URL of the thumbnail version.
        url (str): URL of the webpage containing this similar image.
        image_url (str): Direct URL to the full-size similar image.
    """

    def __init__(self, data: dict[str, Any]):
        self.name: str = data.get("name", "")
        self.thumbnail: str = data.get("thumbnailUrl", "")
        self.url: str = data.get("hostPageUrl", "")
        self.image_url: str = data.get("contentUrl", "")


class Attraction:
    """Represents a tourist attraction identified in the image.

    Attributes:
        url (str): URL to the attraction's information page.
        title (str): Name of the attraction.
        search_url (str): URL for performing a new Bing search about this attraction.
        interest_types (list[str]): Categories or types of interest for this attraction.
    """

    def __init__(self, data: dict[str, Any]):
        self.url: str = data.get("attractionUrl", "")
        self.title: str = data.get("title", "")
        self.search_url: str = data.get("requeryUrl", "")
        self.interest_types: list[str] = data.get("interestTypes", [])


class TravelCard:
    """Represents a travel-related information card from Bing.

    Attributes:
        card_type (str): Type or category of the travel card.
        title (str): Title or heading of the card.
        url (str): URL for more information about this travel topic.
        image_url (str): URL of the main image on the card.
        image_source_url (str): Source URL of the image used in the card.
    """

    def __init__(self, data: dict[str, Any]):
        self.card_type: str = data.get("cardType", "")
        self.title: str = data.get("title", "")
        self.url: str = data.get("clickUrl", "")
        self.image_url: str = data.get("image", "")
        self.image_source_url: str = data.get("imageSourceUrl", "")


class TravelInfo:
    """Contains comprehensive travel information related to the image.

    Attributes:
        destination_name (str): Name of the identified travel destination.
        travel_guide_url (str): URL to Bing's travel guide for this destination.
        attractions (list[Attraction]): List of related tourist attractions.
        travel_cards (list[TravelCard]): Collection of related travel information cards.
    """

    def __init__(self, data: dict[str, Any]):
        self.destination_name: str = data.get("destinationName", "")
        self.travel_guide_url: str = data.get("travelGuideUrl", "")
        self.attractions: list[Attraction] = [Attraction(x) for x in data.get("attractions", [])]
        self.travel_cards: list[TravelCard] = [TravelCard(x) for x in data.get("travelCards", [])]


class EntityItem:
    """Represents an entity (person, place, or thing) identified in the image.

    Attributes:
        name (str): Name of the identified entity.
        thumbnail (str): URL to the entity's thumbnail image.
        description (str): Detailed description of the entity.
        profiles (list[dict]): List of social media profiles, each containing:
            - url (str): Profile URL
            - social_network (str): Name of the social network
        short_description (str): Brief description or entity type.
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

        self.short_description: str = data.get("entityPresentationInfo", {}).get("entityTypeDisplayHint", "")


class BingResponse(BaseSearchResponse[BingItem]):
    """Encapsulates the complete response from a Bing reverse image search.

    This class processes and organizes various types of information returned by Bing's
    image search API, including similar images, related pages, entity information,
    and travel-related data.

    Attributes:
        origin (dict): The raw JSON response data.
        pages_including (list[PagesIncludingItem]): Pages containing the searched image.
        visual_search (list[VisualSearchItem]): Visually similar images.
        related_searches (list[RelatedSearchItem]): Related search suggestions.
        best_guess (Optional[str]): Bing's best guess for what the image represents.
        travel (Optional[TravelInfo]): Travel-related information if applicable.
        entities (list[EntityItem]): Entities identified in the image.
        url (str): URL to the Bing search results page.

    Note:
        The actual content available in the response depends on what Bing's API
        identifies in the searched image. Not all attributes will contain data
        for every search.
    """

    def __init__(self, resp_data: dict[str, Any], resp_url: str, **kwargs: Any):
        """Initialize a Bing search response.

        Args:
            resp_data (dict[str, Any]): The raw JSON response from Bing's API.
            resp_url (str): The URL of the search results page.
            **kwargs (Any): Additional keyword arguments passed to the parent class.
        """
        super().__init__(resp_data, resp_url, **kwargs)

    @override
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
