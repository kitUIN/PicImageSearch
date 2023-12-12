import asyncio

from loguru import logger

from PicImageSearch import Network, TraceMoe
from PicImageSearch.model import TraceMoeResponse
from PicImageSearch.sync import TraceMoe as TraceMoeSync

# proxies = "http://127.0.0.1:1081"
proxies = None
url = "https://raw.githubusercontent.com/kitUIN/PicImageSearch/main/demo/images/test05.jpg"
file = "../images/test05.jpg"


@logger.catch()
async def test_async() -> None:
    async with Network(proxies=proxies) as client:
        tracemoe = TraceMoe(client=client, mute=False, size=None)
        # resp = await tracemoe.search(url=url)
        resp = await tracemoe.search(file=file)
        show_result(resp)


@logger.catch()
def test_sync() -> None:
    tracemoe = TraceMoeSync(proxies=proxies, mute=False, size=None)
    resp = tracemoe.search(url=url)
    # resp = tracemoe.search(file=file)
    show_result(resp)  # type: ignore


def show_result(resp: TraceMoeResponse) -> None:
    # logger.info(resp.origin)  # 原始数据
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
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_async())
    # test_sync()
