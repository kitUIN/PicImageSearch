import asyncio

from demo.code.config import GOOGLE_COOKIES, IMAGE_BASE_URL, PROXIES, get_image_path, logger
from PicImageSearch import GoogleLens, Network
from PicImageSearch.model import GoogleLensExactMatchesItem, GoogleLensExactMatchesResponse, GoogleLensResponse
from PicImageSearch.sync import GoogleLens as GoogleLensSync

url = f"{IMAGE_BASE_URL}/test05.jpg"
file = get_image_path("test05.jpg")


@logger.catch()
async def demo_async() -> None:
    async with Network(proxies=PROXIES, cookies=GOOGLE_COOKIES) as client:
        google_lens_all = GoogleLens(
            client=client,
            search_type="all",
            q="anime",
        )
        resp_all = await google_lens_all.search(url=url)
        show_result(resp_all, search_type="all")

        # google_lens_products = GoogleLens(client=client, search_type="products", q="anime")
        # resp_products = await google_lens_products.search(file=file)
        # show_result(resp_products, search_type="products")

        # google_lens_visual = GoogleLens(client=client, search_type="visual_matches")
        # resp_visual = await google_lens_visual.search(url=url)
        # show_result(resp_visual, search_type="visual_matches")

        # google_lens_exact = GoogleLens(client=client, search_type="exact_matches")
        # resp_exact = await google_lens_exact.search(file=file)
        # show_result(resp_exact, search_type="exact_matches")


@logger.catch()
def demo_sync() -> None:
    google_lens_all = GoogleLensSync(
        proxies=PROXIES,
        cookies=GOOGLE_COOKIES,
        search_type="all",
        q="anime",
    )
    resp_all = google_lens_all.search(url=url)
    show_result(resp_all, search_type="sync_all")  # pyright: ignore[reportArgumentType]

    # google_lens_products = GoogleLensSync(
    #     proxies=PROXIES,
    #     cookies=GOOGLE_COOKIES,
    #     search_type="products",
    #     q="anime",
    # )
    # resp_products = google_lens_products.search(file=file)
    # show_result(resp_products, search_type="products")  # pyright: ignore[reportArgumentType]

    # google_lens_visual = GoogleLensSync(
    #     proxies=PROXIES,
    #     cookies=GOOGLE_COOKIES,
    #     search_type="visual_matches",
    # )
    # resp_visual = google_lens_visual.search(url=url)
    # show_result(resp_visual, search_type="visual_matches")  # pyright: ignore[reportArgumentType]

    # google_lens_exact = GoogleLensSync(
    #     proxies=PROXIES,
    #     cookies=GOOGLE_COOKIES,
    #     search_type="exact_matches",
    # )
    # resp_exact = google_lens_exact.search(file=file)
    # show_result(resp_exact, search_type="exact_matches")  # pyright: ignore[reportArgumentType]


def show_result(resp: GoogleLensResponse | GoogleLensExactMatchesResponse, search_type: str) -> None:
    logger.info(f"Search Type: {search_type}")
    logger.info(f"Search URL: {resp.url}")

    if isinstance(resp, GoogleLensResponse) and resp.related_searches:
        logger.info("Related Searches:")
        for related_search in resp.related_searches:
            logger.info(f"  Title: {related_search.title}")
            logger.info(f"  URL: {related_search.url}")
            logger.info(f"  Thumbnail: {related_search.thumbnail}")
            logger.info("-" * 20)

    if resp.raw:
        match_type = "Visual" if isinstance(resp, GoogleLensResponse) else "Exact"
        logger.info(f"{match_type} Matches:")
        for item in resp.raw:
            logger.info(f"  Title: {item.title}")
            logger.info(f"  URL: {item.url}")
            logger.info(f"  Site Name: {item.site_name}")
            if isinstance(item, GoogleLensExactMatchesItem):
                logger.info(f"  Size: {item.size}")
            logger.info(f"  Thumbnail: {item.thumbnail}")
            logger.info("-" * 20)
    logger.info("-" * 50)


if __name__ == "__main__":
    asyncio.run(demo_async())
    # demo_sync()
