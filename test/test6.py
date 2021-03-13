from PicImageSearch import BaiDu
from loguru import logger

baidu = BaiDu()
res = baidu.search('https://i0.hdslb.com/bfs/article/e756dd0a8375a4c30cc0ee3a51c8067157486135.jpg@1524w_856h.webp')
logger.info(res.item)
logger.info(res.raw[0].title)
logger.info(res.raw[0].page_title)
logger.info(res.raw[0].abstract)
logger.info(res.raw[0].url)
logger.info(res.raw[0].image_src)
