import asyncio

from demo.code.config import IMAGE_BASE_URL, PROXIES, get_image_path, logger
from PicImageSearch import Network, TraceMoe
from PicImageSearch.model import TraceMoeResponse
from PicImageSearch.sync import TraceMoe as TraceMoeSync

url = f"{IMAGE_BASE_URL}/test05.jpg"
file = get_image_path("test05.jpg")


@logger.catch()
async def demo_async() -> None:
    async with Network(proxies=PROXIES) as client:
        tracemoe = TraceMoe(mute=False, size=None, client=client)
        # resp = await tracemoe.search(url=url)
        resp = await tracemoe.search(file=file)
        show_result(resp)


@logger.catch()
def demo_sync() -> None:
    tracemoe = TraceMoeSync(mute=False, size=None, proxies=PROXIES)
    resp = tracemoe.search(url=url)
    # resp = tracemoe.search(file=file)
    show_result(resp)  # pyright: ignore[reportArgumentType]


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
    asyncio.run(demo_async())
    # demo_sync()
