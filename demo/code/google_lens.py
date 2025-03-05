import asyncio
from typing import Union

from demo.code.config import IMAGE_BASE_URL, PROXIES, get_image_path, logger
from PicImageSearch import GoogleLens, Network
from PicImageSearch.model import GoogleLensExactMatchesResponse, GoogleLensResponse
from PicImageSearch.sync import GoogleLens as GoogleLensSync

url = f"{IMAGE_BASE_URL}/test05.jpg"
file = get_image_path("test05.jpg")


@logger.catch()
async def test_async() -> None:
    async with Network(proxies=PROXIES) as client:
        google_lens_all = GoogleLens(
            client=client, search_type="all", q="anime", hl="en", country="US"
        )
        resp_all = await google_lens_all.search(url=url)
        show_result(resp_all, search_type="all")

        # google_lens_products = GoogleLens(client=client, search_type='products', q='anime', hl='en', country='GB')
        # resp_products = await google_lens_products.search(file=file)
        # show_result(resp_products, search_type='products')

        # google_lens_visual = GoogleLens(client=client, search_type='visual_matches', hl='zh', country='CN')
        # resp_visual = await google_lens_visual.search(url=url)
        # show_result(resp_visual, search_type='visual_matches')

        # google_lens_exact = GoogleLens(client=client, search_type='exact_matches', hl='ru', country='RU')
        # resp_exact = await google_lens_exact.search(file=file)
        # show_result(resp_exact, search_type='exact_matches')


@logger.catch()
def test_sync() -> None:
    google_lens_sync_all = GoogleLensSync(proxies=PROXIES, search_type="all", q="anime")
    resp_sync_all = google_lens_sync_all.search(url=url)
    show_result(resp_sync_all, search_type="sync_all")  # pyright: ignore

    google_lens_sync_exact = GoogleLensSync(
        proxies=PROXIES, search_type="exact_matches"
    )
    resp_sync_exact = google_lens_sync_exact.search(file=file)
    show_result(resp_sync_exact, search_type="sync_exact")  # pyright: ignore


def show_result(
    resp: Union[GoogleLensResponse, GoogleLensExactMatchesResponse], search_type: str
) -> None:
    logger.info(f"Search Type: {search_type}")
    logger.info(f"Search URL: {resp.url}")

    if isinstance(resp, GoogleLensResponse):
        if resp.related_searches:
            logger.info("Related Searches:")
            for rs in resp.related_searches:
                logger.info(f"  Title: {rs.title}")
                logger.info(f"  URL: {rs.search_url}")
                logger.info(f"  Image URL: {rs.image_url}")
                logger.info("-" * 20)

        if resp.raw:
            logger.info("Visual Matches:")
            for item in resp.raw:
                logger.info(f"  Title: {item.title}")
                logger.info(f"  URL: {item.url}")
                logger.info(f"  Site Name: {item.site_name}")
                logger.info(f"  Image URL: {item.image_url}")
                logger.info("-" * 20)

    elif resp.raw:
        logger.info("Exact Matches:")
        for item in resp.raw:
            logger.info(f"  Title: {item.title}")
            logger.info(f"  URL: {item.url}")
            logger.info(f"  Site Name: {item.site_name}")
            logger.info(f"  Size: {item.size}")
            logger.info(f"  Image URL: {item.image_url}")
            logger.info("-" * 20)
    logger.info("-" * 50)


if __name__ == "__main__":
    asyncio.run(test_async())
    # test_sync()
