import asyncio
from typing import Optional

from demo.code.config import GOOGLE_COOKIES, IMAGE_BASE_URL, PROXIES, get_image_path, logger
from PicImageSearch import Google, Network
from PicImageSearch.model import GoogleResponse
from PicImageSearch.sync import Google as GoogleSync

url = f"{IMAGE_BASE_URL}/test03.jpg"
file = get_image_path("test03.jpg")
base_url = "https://www.google.co.jp"


@logger.catch()
async def demo_async() -> None:
    async with Network(proxies=PROXIES, cookies=GOOGLE_COOKIES) as client:
        google = Google(base_url=base_url, client=client)
        # resp = await google.search(url=url)
        resp = await google.search(file=file)
        show_result(resp)
        resp2 = await google.next_page(resp)
        show_result(resp2)
        if resp2:
            resp3 = await google.pre_page(resp2)
            show_result(resp3)


@logger.catch()
def demo_sync() -> None:
    google = GoogleSync(base_url=base_url, proxies=PROXIES, cookies=GOOGLE_COOKIES)
    resp = google.search(url=url)
    # resp = google.search(file=file)
    show_result(resp)  # pyright: ignore[reportArgumentType]
    resp2 = google.next_page(resp)  # pyright: ignore[reportArgumentType]
    show_result(resp2)  # pyright: ignore[reportArgumentType]
    if resp2:  # pyright: ignore[reportUnnecessaryComparison]
        resp3 = google.pre_page(resp2)  # pyright: ignore[reportArgumentType]
        show_result(resp3)  # pyright: ignore[reportArgumentType]


def show_result(resp: Optional[GoogleResponse]) -> None:
    if not resp or not resp.raw:
        return
    # logger.info(resp.origin)  # Original Data
    logger.info(resp.pages)
    logger.info(len(resp.pages))
    logger.info(resp.url)  # Link to search results
    logger.info(resp.page_number)

    # try to get first result with thumbnail
    selected = next((i for i in resp.raw if i.thumbnail), resp.raw[0])
    logger.info(selected.origin)
    logger.info(selected.thumbnail)
    logger.info(selected.title)
    logger.info(selected.content)
    logger.info(selected.url)
    logger.info("-" * 50)


if __name__ == "__main__":
    asyncio.run(demo_async())
    # demo_sync()
