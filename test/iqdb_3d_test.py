from loguru import logger
from PicImageSearch import Iqdb

# 如果需要代理
_REQUESTS_KWARGS = {
    "proxies": {
        "https": "http://127.0.0.1:8888",
    }
}
iqdb = Iqdb()
res = iqdb.search_3d(
    "https://3d.iqdb.org/3dbooru/2/8/6/2865ab9c1d9fe8860892945e79435219.jpg"
)

# logger.info(res.origin)
# logger.info(res.raw)
logger.info("说明:              " + res.raw[0].content)
logger.info("来源地址:          " + res.raw[0].url)
logger.info("缩略图:            " + res.raw[0].thumbnail)
logger.info("相似度:            " + res.raw[0].similarity)
logger.info("图片大小:          " + res.raw[0].size)
logger.info("图片来源:          " + res.raw[0].source)
logger.info("其他图片来源:      " + str(res.raw[0].other_source))
logger.info("相似度低的结果:    " + str(res.more))
