import asyncio

from loguru import logger

from PicImageSearch import Network, SauceNAO
from PicImageSearch.model import SauceNAOResponse
from PicImageSearch.sync import SauceNAO as SauceNAOSync

# proxies = "http://127.0.0.1:1081"
proxies = None
url = "https://raw.githubusercontent.com/kitUIN/PicImageSearch/main/demo/images/test01.jpg"
file = "../images/test01.jpg"
api_key = "a4ab3f81009b003528f7e31aed187fa32a063f58"


@logger.catch()
async def test_async() -> None:
    async with Network(proxies=proxies) as client:
        saucenao = SauceNAO(client=client, api_key=api_key, hide=3)
        # resp = await saucenao.search(url=url)
        resp = await saucenao.search(file=file)
        show_result(resp)


@logger.catch()
def test_sync() -> None:
    saucenao = SauceNAOSync(proxies=proxies, api_key=api_key, hide=3)
    resp = saucenao.search(url=url)
    # resp = saucenao.search(file=file)
    show_result(resp)  # type: ignore


def show_result(resp: SauceNAOResponse) -> None:
    logger.info(resp.status_code)  # HTTP status
    logger.info(resp.origin)  # Original Data
    logger.info(resp.url)  # Link to search results
    logger.info(resp.raw[0].origin)
    logger.info(resp.long_remaining)
    logger.info(resp.short_remaining)
    logger.info(resp.raw[0].thumbnail)
    logger.info(resp.raw[0].similarity)
    logger.info(resp.raw[0].hidden)
    logger.info(resp.raw[0].title)
    logger.info(resp.raw[0].author)
    logger.info(resp.raw[0].author_url)
    logger.info(resp.raw[0].source)
    logger.info(resp.raw[0].url)
    logger.info(resp.raw[0].ext_urls)
    logger.info("-" * 50)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_async())
    # test_sync()
