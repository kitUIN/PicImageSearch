from loguru import logger
from PicImageSearch import Iqdb
_REQUESTS_KWARGS = {
    # 'proxies': {
    #     'https': 'http://127.0.0.1:10809',
    # }
    # 如果需要代理
}
iqdb = Iqdb()
result = iqdb.search('https://ascii2d.net/thumbnail/b/4/a/e/b4ae7762f6d247e04bba6b925ce5f6d1.jpg')
res = result.raw[0]
logger.info(res.content)    # Best match
logger.info(res.url)        # https://yande.re/post/show/681461
logger.info(res.thumbnail)  # http://www.iqdb.org/moe.imouto/2/8/b/28beb871b6b162196cd1e4957a2ce5f5.jpg
logger.info(res.similarity) # 95% similarity
logger.info(res.size)       # 3938×6276 [Ero]
logger.info(res.title)      # Rating: q Score: 8 Tags: bikini_top fate/grand_order hews nipples open_shirt saber_extra see_through swimsuits
