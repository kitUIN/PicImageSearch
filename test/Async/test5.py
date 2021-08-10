import asyncio

from loguru import logger

from PicImageSearch import AsyncGoogle, NetWork


async def main():
    async with NetWork(proxy='http://127.0.0.1:10809') as client:
        google = AsyncGoogle(client=client)
        res = await google.search("https://media.discordapp.net/attachments/783138508038471701/813452582948306974/hl-18-1-900x1280.png?width=314&height=447")
        # res = google.search(r'C:/kitUIN/img/tinted-good.jpg')  # Search Image URL or path
        logger.info(res.origin)  # Original Data
        logger.info(res.raw.__str__())  # Raw Data
        # Should start from index 2, because from there is matching image
        logger.info(res.raw[2])  # <NormGoogle(title=["The Strongest Dull Prince's Secret Battle for the Throne ..."], urls=['https://kiryuu.co/the-strongest-dull-princes-secret-battle-for-the-throne-chapter-3-bahasa-indonesia/'], thumbnail=['No directable url'])>
        logger.info(res.raw[2].thumbnail)  # No directable url
        logger.info(res.raw[2].title)  # The Strongest Dull Prince's Secret Battle for the Throne ...
        logger.info(res.raw[2].url)  # https://kiryuu.co/the-strongest-dull-princes-secret-battle-for-the-throne-chapter-3-bahasa-indonesia/


loop = asyncio.new_event_loop()
loop.run_until_complete(main())