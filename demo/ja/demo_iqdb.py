import asyncio

from loguru import logger

from src import Iqdb, Network
from src.model import IqdbResponse
from src.sync import Iqdb as IqdbSync

# proxies = "http://127.0.0.1:1081"
proxies = None
url = "https://raw.githubusercontent.com/kitUIN/PicImageSearch/main/demo/images/test01.jpg"
file = "../images/test01.jpg"


@logger.catch()
async def test_async() -> None:
    async with Network(proxies=proxies) as client:
        iqdb = Iqdb(client=client)
        # resp = await iqdb.search(url=url)
        resp = await iqdb.search(file=file)
        show_result(resp)


@logger.catch()
def test_sync() -> None:
    iqdb = IqdbSync(proxies=proxies)
    resp = iqdb.search(url=url)
    # resp = iqdb.search(file=file)
    show_result(resp)  # type: ignore


def show_result(resp: IqdbResponse) -> None:
    # logger.info(resp.origin)  # オリジナルデータ
    logger.info(resp.url)  # 検索結果へのリンク
    # logger.info(resp.raw[0].origin)
    logger.info(f"説明: {resp.raw[0].content}")
    logger.info(f"ソース URL: {resp.raw[0].url}")
    logger.info(f"サムネイル: {resp.raw[0].thumbnail}")
    logger.info(f"類似度: {resp.raw[0].similarity}")
    logger.info(f"画像サイズ: {resp.raw[0].size}")
    logger.info(f"画像ソース: {resp.raw[0].source}")
    logger.info(f"他の画像ソース: {resp.raw[0].other_source}")
    logger.info(f"SauceNAO 検索リンク: {resp.saucenao_url}")
    logger.info(f"Ascii2d 検索リンク: {resp.ascii2d_url}")
    logger.info(f"TinEye 検索リンク: {resp.tineye_url}")
    logger.info(f"Google 検索リンク: {resp.google_url}")
    logger.info(f"低い類似度の結果の数: {len(resp.more)}")
    logger.info("-" * 50)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_async())
    # test_sync()
