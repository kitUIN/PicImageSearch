from loguru import logger

from PicImageSearch import Ascii2D

ascii2d = Ascii2D()
res = ascii2d.search('https://pixiv.cat/77702503-1.jpg')
#res = ascii2d.search(r'C:/kitUIN/img/tinted-good.jpg')  # 搜索本地图片
logger.info(res.origin)  # 原始数据
logger.info(res.raw)  #
logger.info(res.raw[1])  # <NormAscii2D(title=['2020.08.30'], authors=['hews__'],mark=['twitter'])>
logger.info(res.raw[1].thumbnail[0])  # https://ascii2d.net/thumbnail/2/c/5/e/2c5e6a18fbba730a65cef0549e3c5768.jpg
logger.info(res.raw[1].titles[0])  # 2020.08.30
logger.info(res.raw[1].authors[0])  # hews__
logger.info(res.raw[1].urls[0])  # https://twitter.com/hews__/status/1299728221005643776
logger.info(res.raw[1].detail)  # 2570x4096 JPEG 1087.9KB
