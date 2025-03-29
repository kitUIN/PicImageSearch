import asyncio

from demo.code.config import IMAGE_BASE_URL, PROXIES, get_image_path, logger
from PicImageSearch import AnimeTrace, Network
from PicImageSearch.model import AnimeTraceResponse
from PicImageSearch.sync import AnimeTrace as AnimeTraceSync

url = f"{IMAGE_BASE_URL}/test05.jpg"
file = get_image_path("test05.jpg")


@logger.catch()
async def demo_async() -> None:
    async with Network(proxies=PROXIES) as client:
        anime_trace = AnimeTrace(client=client)
        resp = await anime_trace.search(url=url)
        # resp = await anime_trace.search(file=file)
        show_result(resp)


@logger.catch()
def demo_sync() -> None:
    anime_trace = AnimeTraceSync(proxies=PROXIES)
    # resp = anime_trace.search(url=url)
    resp = anime_trace.search(file=file)
    show_result(resp)  # pyright: ignore[reportArgumentType]


def show_result(resp: AnimeTraceResponse) -> None:
    # logger.info(resp.origin)
    logger.info(resp.code)
    logger.info(resp.ai)
    logger.info(resp.trace_id)

    if resp.raw:
        # logger.info(resp.raw[0].origin)
        logger.info(resp.raw[0].box)
        logger.info(resp.raw[0].box_id)
        if characters := resp.raw[0].characters:
            for character in characters:
                logger.info(f"Character Name: {character.name}")
                logger.info(f"From Work: {character.work}")


if __name__ == "__main__":
    asyncio.run(demo_async())
    # demo_sync()
