import asyncio

from demo.code.config import IMAGE_BASE_URL, PROXIES, get_image_path, logger
from PicImageSearch import Lenso, Network
from PicImageSearch.model import LensoResponse
from PicImageSearch.sync import Lenso as LensoSync

url = f"{IMAGE_BASE_URL}/test08.jpg"
file = get_image_path("test08.jpg")

search_types = ["", "similar", "duplicates", "places", "related"]
sort_types = ["SMART", "RANDOM", "QUALITY_DESCENDING", "QUALITY_ASCENDING", "DATE_DESCENDING", "DATE_ASCENDING"]

DEFAULT_SEARCH_TYPE = search_types[0]
DEFAULT_SORT_TYPE = sort_types[0]

@logger.catch()
async def test_async() -> None:
    async with Network(proxies=PROXIES) as client:
        lenso = Lenso(client=client)
        resp = await lenso.search(file=file, search_type=DEFAULT_SEARCH_TYPE, sort_type=DEFAULT_SORT_TYPE)
        show_result(resp, DEFAULT_SEARCH_TYPE)


@logger.catch()
def test_sync() -> None:
    lenso = LensoSync(proxies=PROXIES)
    resp = lenso.search(file=file, search_type=DEFAULT_SEARCH_TYPE, sort_type=DEFAULT_SORT_TYPE)
    show_result(resp, DEFAULT_SEARCH_TYPE)


def show_result(resp: LensoResponse, search_type: str) -> None:
    logger.info(f"Search Type: {search_type}")
    logger.info(f"Search URL: {resp.url}")

    result_lists = {
        "similar": resp.similar,
        "duplicates": resp.duplicates,
        "places": resp.places,
        "related": resp.related,
    }

    for res_type, items in result_lists.items():
        if items:
            logger.info(f"\n--- {res_type} Results ---")
            for item in items:
                logger.info(f"  Hash: {item.hash}")
                logger.info(f"  Similarity: {item.similarity}")
                logger.info(f"  Image Proxy URL: {item.image_proxy_url}")
                logger.info(f"  Image Size: {item.width}x{item.height}")
                logger.info("  URLs:")
                for url_item in item.url_list:
                    logger.info(f"    > Image URL: {url_item.image_url}")
                    logger.info(f"    > Source URL: {url_item.source_url}")
                    logger.info(f"    > Title: {url_item.title}")
                    logger.info(f"    > Lang: {url_item.lang}")
                logger.info("-" * 20)
        else:
            logger.info(f"\n--- No {res_type} Results ---")

    logger.info("=" * 50)


if __name__ == "__main__":
    asyncio.run(test_async())
    # test_sync()
