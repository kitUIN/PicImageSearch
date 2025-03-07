import asyncio
from typing import Optional

from demo.code.config import IMAGE_BASE_URL, PROXIES, get_image_path, logger
from PicImageSearch import Google, Network
from PicImageSearch.model import GoogleResponse
from PicImageSearch.sync import Google as GoogleSync

url = f"{IMAGE_BASE_URL}/test03.jpg"
file = get_image_path("test03.jpg")
base_url = "https://www.google.co.jp"

# Note: Google search requires the `NID` cookie (when NOT logged into any Google account), expected format: `NID=...`
cookies: Optional[str] = None


@logger.catch()
async def test_async() -> None:
    async with Network(proxies=PROXIES, cookies=cookies) as client:
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
def test_sync() -> None:
    google = GoogleSync(base_url=base_url, proxies=PROXIES, cookies=cookies)
    resp = google.search(url=url)
    # resp = google.search(file=file)
    show_result(resp)  # type: ignore
    resp2 = google.next_page(resp)  # type: ignore
    show_result(resp2)  # type: ignore
    if resp2:
        resp3 = google.pre_page(resp2)  # type: ignore
        show_result(resp3)  # type: ignore


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
    logger.info(selected.url)
    logger.info("-" * 50)


if __name__ == "__main__":
    asyncio.run(test_async())
    # test_sync()
