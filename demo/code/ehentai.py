import asyncio
from pathlib import Path

from loguru import logger

from PicImageSearch import EHentai, Network
from PicImageSearch.model import EHentaiResponse
from PicImageSearch.sync import EHentai as EHentaiSync

proxies = "http://127.0.0.1:1080"
# proxies = None
url = "https://raw.githubusercontent.com/kitUIN/PicImageSearch/main/demo/images/test06.jpg"
file = Path(__file__).parent.parent / "images" / "test06.jpg"

# Note: EXHentai search requires cookies if to be used
cookies = None

# Use EXHentai search or not, it's recommended to use bool(cookies), i.e. use EXHentai search if cookies is configured
is_ex = False

# Whenever possible, avoid timeouts that return an empty document
timeout = 60


@logger.catch()
async def test_async() -> None:
    async with Network(proxies=proxies, cookies=cookies, timeout=timeout) as client:
        ehentai = EHentai(is_ex=is_ex, client=client)
        # resp = await ehentai.search(url=url)
        resp = await ehentai.search(file=file)
        show_result(resp)


@logger.catch()
def test_sync() -> None:
    ehentai = EHentaiSync(
        is_ex=is_ex,
        proxies=proxies,
        cookies=cookies,
        timeout=timeout,
    )
    resp = ehentai.search(url=url)
    # resp = ehentai.search(file=file)
    show_result(resp)  # type: ignore


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
    asyncio.run(test_async())
    # test_sync()
