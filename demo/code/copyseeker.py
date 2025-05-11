import asyncio

from demo.code.config import IMAGE_BASE_URL, PROXIES, get_image_path, logger
from PicImageSearch import Copyseeker, Network
from PicImageSearch.model import CopyseekerResponse
from PicImageSearch.sync import Copyseeker as CopyseekerSync

url = f"{IMAGE_BASE_URL}/test05.jpg"
file = get_image_path("test05.jpg")


@logger.catch()
async def demo_async() -> None:
    async with Network(proxies=PROXIES) as client:
        copyseeker = Copyseeker(client=client)
        # resp = await copyseeker.search(url=url)
        resp = await copyseeker.search(file=file)
        show_result(resp)


@logger.catch()
def demo_sync() -> None:
    # Note: Unlike other modules, Copyseeker requires special handling in sync mode
    # due to its multi-step API that depends on persistent cookies between requests.
    #
    # The standard syncified wrapper doesn't maintain client state properly for such APIs,
    # because each request may create a new client instance, losing cookie state.
    #
    # This explicit client management approach ensures cookies persist across requests.
    # This complexity is one reason why async methods are generally recommended over sync methods.
    network = Network(proxies=PROXIES)
    client = network.start()

    # Pass the client explicitly to maintain the same session across multiple requests
    copyseeker = CopyseekerSync(client=client)
    resp = copyseeker.search(url=url)
    # resp = copyseeker.search(file=file)

    # Important: We need to properly close the network client to avoid resource leaks
    # This step isn't necessary with context managers in async code (async with Network() as client:)
    network.close()

    show_result(resp)  # pyright: ignore[reportArgumentType]


def show_result(resp: CopyseekerResponse) -> None:
    logger.info(resp.id)
    logger.info(resp.image_url)
    logger.info(resp.best_guess_label)
    logger.info(resp.entities)
    logger.info(resp.total)
    logger.info(resp.exif)
    logger.info(resp.similar_image_urls)
    if resp.raw:
        logger.info(resp.raw[0].url)
        logger.info(resp.raw[0].title)
        logger.info(resp.raw[0].website_rank)
        logger.info(resp.raw[0].thumbnail)
        logger.info(resp.raw[0].thumbnail_list)
    logger.info("-" * 50)
    # logger.info(resp.visuallySimilarImages)


if __name__ == "__main__":
    asyncio.run(demo_async())
    # demo_sync()
