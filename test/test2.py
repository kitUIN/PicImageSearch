from loguru import logger

from PicImageSeach.saucenao import SauceNAO

saucenao = SauceNAO()
a = saucenao.search('https://cdn.jsdelivr.net/gh/laosepi/setu/pics_original/77702503_p0.jpg')
logger.info(a.origin)  # 原始数据
logger.info(a.raw)  #
logger.info(a.raw[0])  #
logger.info(a.long_remaining)  # 99
logger.info(a.short_remaining)  # 3
logger.info(a.raw[0].thumbnail)  # https://img1.saucenao.com/res/pixiv/7770/77702503_p0_master1200.jpg?auth=pJmiu8qNI1z2fLBAlAsx7A&exp=1604748473
logger.info(a.raw[0].similarity)  # 92.22
logger.info(a.raw[0].title)  # MDR♡
logger.info(a.raw[0].author)  # CeNanGam
logger.info(a.raw[0].pixiv_id)  # 77702503
logger.info(a.raw[0].member_id)  # 4089680
