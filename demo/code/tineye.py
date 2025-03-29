import asyncio
from typing import Optional

from demo.code.config import IMAGE_BASE_URL, PROXIES, get_image_path, logger
from PicImageSearch import Network, Tineye
from PicImageSearch.model import TineyeItem, TineyeResponse
from PicImageSearch.sync import Tineye as TineyeSync

url = f"{IMAGE_BASE_URL}/test07.jpg"
file = get_image_path("test07.jpg")

# TinEye search parameters
show_unavailable_domains = False
domain = ""  # Example: domain='wikipedia.org'
tags = ""  # Example: tags="stock,collection"
sort = "score"  # Example: "size" or "crawl_date"
order = "desc"  # Example: "asc"


@logger.catch()
async def demo_async() -> None:
    async with Network(proxies=PROXIES) as client:
        tineye = Tineye(client=client)
        # resp = await tineye.search(
        #     url=url,
        #     show_unavailable_domains=show_unavailable_domains,
        #     domain=domain,
        #     tags=tags,
        #     sort=sort,
        #     order=order,
        # )
        resp = await tineye.search(
            file=file,
            show_unavailable_domains=show_unavailable_domains,
            domain=domain,
            tags=tags,
            sort=sort,
            order=order,
        )
        show_result(resp, "Initial Search")

        if resp.total_pages > 1:
            resp2 = await tineye.next_page(resp)
            show_result(resp2, "Next Page")

            if resp2:
                resp3 = await tineye.next_page(resp2)
                show_result(resp3, "Next Page")

                if resp3:
                    resp4 = await tineye.pre_page(resp3)
                    show_result(resp4, "Previous Page")


@logger.catch()
def demo_sync() -> None:
    tineye = TineyeSync(proxies=PROXIES)
    resp = tineye.search(
        url=url,
        show_unavailable_domains=show_unavailable_domains,
        domain=domain,
        tags=tags,
        sort=sort,
        order=order,
    )
    # resp = tineye.search(
    #     file=file,
    #     show_unavailable_domains=show_unavailable_domains,
    #     domain=domain,
    #     tags=tags,
    #     sort=sort,
    #     order=order,
    # )
    show_result(resp, "Initial Search")  # pyright: ignore[reportArgumentType]

    if resp.total_pages > 1:  # pyright: ignore[reportAttributeAccessIssue]
        resp2 = tineye.next_page(resp)  # pyright: ignore[reportArgumentType]
        show_result(resp2, "Next Page")  # pyright: ignore[reportArgumentType]

        if resp2:  # pyright: ignore[reportUnnecessaryComparison]
            resp3 = tineye.next_page(resp2)  # pyright: ignore[reportArgumentType]
            show_result(resp3, "Next Page")  # pyright: ignore[reportArgumentType]

            if resp3:  # pyright: ignore[reportUnnecessaryComparison]
                resp4 = tineye.pre_page(resp3)  # pyright: ignore[reportArgumentType]
                show_result(resp4, "Previous Page")  # pyright: ignore[reportArgumentType]


def show_result(resp: Optional[TineyeResponse], title: str = "") -> None:
    if resp and not resp.raw:
        logger.info(f"Origin Response: {resp.origin}")

    if not resp or not resp.raw:
        logger.info(f"{title}: No results found.")
        return
    # logger.info(f"Domains: {resp.domains}")
    logger.info(f"{title}:")
    logger.info(f"  Status Code: {resp.status_code}")
    logger.info(f"  Query Hash: {resp.query_hash}")  # image hash
    logger.info(f"  Total Pages: {resp.total_pages}")
    logger.info(f"  Current Page: {resp.page_number}")
    logger.info("  Results:")

    for i, item in enumerate(resp.raw):
        show_match_details(i, item)


def show_match_details(match_index: int, match_item: TineyeItem) -> None:
    logger.info(f"    Match {match_index + 1}:")
    logger.info(f"      Thumbnail URL: {match_item.thumbnail}")
    logger.info(f"      Image URL: {match_item.image_url}")
    logger.info(f"      URL(Backlink): {match_item.url}")
    logger.info(f"      Domain: {match_item.domain}")
    logger.info(f"      Size: {match_item.size[0]}x{match_item.size[1]}")
    logger.info(f"      Crawl Date: {match_item.crawl_date}")
    logger.info("-" * 50)


if __name__ == "__main__":
    asyncio.run(demo_async())
    # demo_sync()
