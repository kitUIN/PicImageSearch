import asyncio
from typing import Optional

from demo.code.config import IMAGE_BASE_URL, PROXIES, get_image_path, logger
from PicImageSearch import EHentai, Network
from PicImageSearch.model import EHentaiResponse
from PicImageSearch.sync import EHentai as EHentaiSync

url = f"{IMAGE_BASE_URL}/test06.jpg"
file = get_image_path("test06.jpg")

# Note: EXHentai search requires cookies if to be used
cookies: Optional[str] = None

# Use EXHentai search or not, it's recommended to use bool(cookies), i.e. use EXHentai search if cookies is configured
is_ex = False

# Whenever possible, avoid timeouts that return an empty document
timeout = 60


@logger.catch()
async def demo_async() -> None:
    async with Network(proxies=PROXIES, cookies=cookies, timeout=timeout) as client:
        ehentai = EHentai(is_ex=is_ex, client=client)
        # resp = await ehentai.search(url=url)
        resp = await ehentai.search(file=file)
        show_result(resp)


@logger.catch()
def demo_sync() -> None:
    ehentai = EHentaiSync(
        is_ex=is_ex,
        proxies=PROXIES,
        cookies=cookies,
        timeout=timeout,
    )
    resp = ehentai.search(url=url)
    # resp = ehentai.search(file=file)
    show_result(resp)  # pyright: ignore[reportArgumentType]


def show_result(resp: EHentaiResponse) -> None:
    # logger.info(resp.origin)  # Original data
    logger.info(resp.url)  # Link to search results
    # logger.info(resp.raw[0].origin)
    logger.info(resp.raw[0].title)
    logger.info(resp.raw[0].url)
    logger.info(resp.raw[0].thumbnail)
    logger.info(resp.raw[0].type)
    logger.info(resp.raw[0].date)

    # It is recommended to use the Compact / Extended page layout, otherwise you will not get tags
    logger.info(resp.raw[0].tags)
    logger.info("-" * 50)


if __name__ == "__main__":
    asyncio.run(demo_async())
    # demo_sync()
