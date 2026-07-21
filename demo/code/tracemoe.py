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
    result = resp.raw[0]
    logger.info(result.origin)
    logger.info(result.anime_info)
    logger.info(resp.frameCount)
    logger.info(result.anilist_id)
    logger.info(result.idMal)
    logger.info(result.title_native)
    logger.info(result.title_romaji)
    logger.info(result.title_english)
    logger.info(result.title_chinese)
    logger.info(result.synonyms)
    logger.info(result.isAdult)
    logger.info(result.type)
    logger.info(result.format)
    logger.info(result.start_date)
    logger.info(result.end_date)
    logger.info(result.cover_image)
    logger.info(result.filename)
    logger.info(result.episode)
    logger.info(result.From)
    logger.info(result.To)
    logger.info(result.similarity)
    logger.info(result.video)
    logger.info(result.image)


if __name__ == "__main__":
    asyncio.run(demo_async())
    # demo_sync()
