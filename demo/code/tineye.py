import asyncio
import mimetypes
from pathlib import Path
from typing import Optional

from loguru import logger

from PicImageSearch import Network, Tineye
from PicImageSearch.model import TineyeResponse
from PicImageSearch.sync import Tineye as TineyeSync

# proxies = "http://127.0.0.1:1080"
proxies = None
url = "https://raw.githubusercontent.com/kitUIN/PicImageSearch/main/demo/images/test02.jpg"
file = Path(__file__).parent.parent / "images" / "test07.jpg"

# TinEye search parameters
show_unavailable_domains = False # Example: show_unavailable_domains=True
domain = ""  # Example: domain='wikipedia.org'
tags = ""  # Example: tags="stock,collection"
sort = "score"  # Example: "size" or "crawl_date"
order = "desc" # Example: "asc"


@logger.catch()
async def test_async() -> None:
    async with Network(proxies=proxies) as client:
        tineye = Tineye(client=client)
        # resp = await tineye.search(url=url, show_unavailable_domains=show_unavailable_domains, domain=domain, tags=tags, sort=sort, order=order)
        resp = await tineye.search(file=file, show_unavailable_domains=show_unavailable_domains, domain=domain, tags=tags, sort=sort, order=order)
        show_result(resp, "Initial Search")

        if resp.pages and len(resp.pages) > 1:  # type: ignore
            resp2 = await tineye.next_page(resp)  # type: ignore
            show_result(resp2, "Next Page (Async)")

            if resp2:
                resp3 = await tineye.next_page(resp2)  # type: ignore
                show_result(resp3, "Next Page (Async)")

                if resp3:
                    resp4 = await tineye.pre_page(resp3)  # type: ignore
                    show_result(resp4, "Previous Page (Async)")


@logger.catch()
def test_sync() -> None:
    tineye = TineyeSync(proxies=proxies)
    resp = tineye.search(url=url, show_unavailable_domains=show_unavailable_domains, domain=domain, tags=tags, sort=sort, order=order)
    # resp = tineye.search(file=file)
    show_result(resp, "Initial Search (Sync)")

    if resp.pages and len(resp.pages) > 1:  # type: ignore
        resp2 = tineye.next_page(resp)  # type: ignore
        show_result(resp2, "Next Page (Sync)")

        if resp2:
            resp3 = tineye.next_page(resp2)  # type: ignore
            show_result(resp3, "Next Page (Sync)")

            if resp3:
                resp4 = tineye.pre_page(resp3)  # type: ignore
                show_result(resp4, "Previous Page (Sync)")


def show_result(resp: Optional[TineyeResponse], title: str = "") -> None:
    if not resp or not resp.raw:
        logger.info(f"{title}: No results found.")
        return
    # logger.info(f"Domains: {resp.domains}")
    logger.info(f"{title}:")
    logger.info(f"  Status Code: {resp.status_code}")
    logger.info(f"  Query Hash: {resp.query_hash}") # image hash
    logger.info(f"  Total Pages: {len(resp.pages)}")  # type: ignore
    logger.info(f"  Current Page: {resp.page_number}")
    logger.info(f"  Results:")

    for i, item in enumerate(resp.raw):
        logger.info(f"    Match {i + 1}:")
        logger.info(f"      Thumbnail URL: {item.thumbnail}")
        logger.info(f"      Image URL: {item.image_url}")
        logger.info(f"      URL(Backlink): {item.url}")
        logger.info(f"      Domain: {item.domain}")
        logger.info(f"      Size: {item.size[0]}x{item.size[1]}")
        logger.info(f"      Crawl Date: {item.crawl_date}")
        logger.info("-" * 40)


if __name__ == "__main__":
    asyncio.run(test_async())
    # test_sync()