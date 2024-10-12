import asyncio

from loguru import logger

from PicImageSearch import Copyseeker, Network
from PicImageSearch.model import CopyseekerResponse
from PicImageSearch.sync import Copyseeker as CopyseekerSync

# proxies = "http://127.0.0.1:1081"
proxies = None
url = (
    "https://github.com/kitUIN/PicImageSearch/blob/main/demo/images/test05.jpg?raw=true"
)
file = "../images/test05.jpg"


@logger.catch()
async def test_async() -> None:
    async with Network(proxies=proxies) as client:
        copyseeker = Copyseeker(client=client)
        # resp = await copyseeker.search(url=url)
        resp = await copyseeker.search(file=file)
        show_result(resp)


@logger.catch()
def test_sync() -> None:
    copyseeker = CopyseekerSync(proxies=proxies)
    resp = copyseeker.search(url=url)
    # resp = copyseeker.search(file=file)
    show_result(resp)  # type: ignore


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
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_async())
    # test_sync()
