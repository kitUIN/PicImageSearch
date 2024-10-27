import asyncio
from pathlib import Path

from loguru import logger

from PicImageSearch import Network, TraceMoe
from PicImageSearch.model import TraceMoeResponse
from PicImageSearch.sync import TraceMoe as TraceMoeSync

# proxies = "http://127.0.0.1:1080"
proxies = None
url = "https://raw.githubusercontent.com/kitUIN/PicImageSearch/main/demo/images/test05.jpg"
file = Path(__file__).parent.parent / "images" / "test05.jpg"


@logger.catch()
async def test_async() -> None:
    async with Network(proxies=proxies) as client:
        tracemoe = TraceMoe(mute=False, size=None, client=client)
        # resp = await tracemoe.search(url=url)
        resp = await tracemoe.search(file=file)
        show_result(resp)


@logger.catch()
def test_sync() -> None:
    tracemoe = TraceMoeSync(mute=False, size=None, proxies=proxies)
    resp = tracemoe.search(url=url)
    # resp = tracemoe.search(file=file)
    show_result(resp)  # type: ignore


def show_result(resp: TraceMoeResponse) -> None:
    # logger.info(resp.origin)  # Original Data
    logger.info(resp.raw[0].origin)
    logger.info(resp.raw[0].anime_info)
    logger.info(resp.frameCount)
    logger.info(resp.raw[0].anilist)
    logger.info(resp.raw[0].idMal)
    logger.info(resp.raw[0].title_native)
    logger.info(resp.raw[0].title_romaji)
    logger.info(resp.raw[0].title_english)
    logger.info(resp.raw[0].title_chinese)
    logger.info(resp.raw[0].synonyms)
    logger.info(resp.raw[0].isAdult)
    logger.info(resp.raw[0].type)
    logger.info(resp.raw[0].format)
    logger.info(resp.raw[0].start_date)
    logger.info(resp.raw[0].end_date)
    logger.info(resp.raw[0].cover_image)
    logger.info(resp.raw[0].filename)
    logger.info(resp.raw[0].episode)
    logger.info(resp.raw[0].From)
    logger.info(resp.raw[0].To)
    logger.info(resp.raw[0].similarity)
    logger.info(resp.raw[0].video)
    logger.info(resp.raw[0].image)


if __name__ == "__main__":
    asyncio.run(test_async())  # type: ignore
    # test_sync()  # type: ignore
