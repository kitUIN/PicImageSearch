#! /usr/bin/env python3
# coding=utf-8
from loguru import logger

from PicImageSearch.saucenao import SauceNAO

_REQUESTS_KWARGS = {
    # 'proxies': {
    #     'https': 'http://127.0.0.1:10809',
    # }
    # 如果需要代理
}
saucenao = SauceNAO(api_key='54a8d90c583d3b66b6dd3d7e9001a39b588cd842', testmode=1, **_REQUESTS_KWARGS)
res = saucenao.search('https://cdn.jsdelivr.net/gh/laosepi/setu/pics_original/77702503_p0.jpg')
#res = saucenao.search(r'C:/kitUIN/img/tinted-good.jpg')#搜索本地图片
# saucenao.download_thumbnail(res.raw[0].thumbnail) 下载缩略图
logger.info(res.origin)  # 原始数据
logger.info(res.raw)  #
logger.info(res.raw[0])  #
logger.info(res.long_remaining)  # 99
logger.info(res.short_remaining)  # 3
logger.info(res.raw[0].thumbnail)  # https://img1.saucenao.com/res/pixiv/7770/77702503_p0_master1200.jpg?auth=pJmiu8qNI1z2fLBAlAsx7A&exp=1604748473
logger.info(res.raw[0].similarity)  # 92.22
logger.info(res.raw[0].title)  # MDR♡
logger.info(res.raw[0].author)  # CeNanGam
logger.info(res.raw[0].url)  # https://www.pixiv.net/member_illust.php?mode=medium&illust_id=77702503
logger.info(res.raw[0].pixiv_id)  # 77702503
logger.info(res.raw[0].member_id)  # 4089680
