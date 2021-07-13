from loguru import logger
from PicImageSearch.tracemoe import TraceMoe

tracemoe = TraceMoe(mute=False)
# res = tracemoe.search('https://trace.moe/img/tinted-good.jpg')# 搜索网络图片
res = tracemoe.search(r'C:/Users/kulujun/Pictures/1.png')  # 搜索本地图片
logger.info(res.origin)
logger.info(res.raw)
logger.info(res.raw[0])
logger.info(res.frameCount)
logger.info(res.raw[0].anilist)
logger.info(res.raw[0].filename)
logger.info(res.raw[0].episode)
logger.info(res.raw[0].From)
logger.info(res.raw[0].To)
logger.info(res.raw[0].similarity)
logger.info(res.raw[0].video)
logger.info(res.raw[0].image)
logger.info(res.raw[0].download_image())
logger.info(res.raw[0].download_video())
logger.info(tracemoe.me())
# ---------------过时版本-----------------------
# logger.info(res.origin)
# logger.info(res.raw)  # [<NormTraceMoe(title='心連·情結', similarity=0.97)>, <NormTraceMoe(title='涼宮春日的憂鬱', similarity=0.82)>, <NormTraceMoe(title='涼宮春日的憂鬱 2009', similarity=0.82)>, <NormTraceMoe(title='鑽石王牌 第二季', similarity=0.82)>, <NormTraceMoe(title='Soul Link', similarity=0.81)>, <NormTraceMoe(title='神之見習者秘密的心靈蛋', similarity=0.81)>, <NormTraceMoe(title='銀狐', similarity=0.81)>, <NormTraceMoe(title='驅魔少年', similarity=0.81)>]
# logger.info(res.raw[0])  # <NormTraceMoe(title='心連·情結', similarity=0.97)>
# logger.info(res.RawDocsCount)  # 5718114
# logger.info(res.RawDocsSearchTime)  # 15530
# logger.info(res.ReRankSearchTime)  # 1167
# logger.info(res.trial)  # 1
# logger.info(res.raw[0].thumbnail)  # https://trace.moe/thumbnail.php?anilist_id=11887&file=%5BANK-Raws%26NatsuYuki%5D%20Kokoro%20Connect%20-%2005%20%28BDrip%201280x720%20x264%20AAC%29.mp4&t=1174.5&token=I7RtV-BVFDjvgwgPpUwFKw
# logger.info(res.raw[0].video_thumbnail)  # https://media.trace.moe/video/11887/%5BANK-Raws%26NatsuYuki%5D%20Kokoro%20Connect%20-%2005%20%28BDrip%201280x720%20x264%20AAC%29.mp4?t=1174.5&token=I7RtV-BVFDjvgwgPpUwFKw
# logger.info(res.raw[0].similarity)  # 0.9685373563005802
# logger.info(res.raw[0].From)  # 1173.83
# logger.info(res.raw[0].To)  # 1174.67
# logger.info(res.raw[0].at)  # 1174.5
# logger.info(res.raw[0].anilist_id)  # 11887
# logger.info(res.raw[0].season)  # 2012-07
# logger.info(res.raw[0].anime)  # 心連·情結
# logger.info(res.raw[0].title)  # ココロコネクト
# logger.info(res.raw[0].title_native)  # ココロコネクト
# logger.info(res.raw[0].title_chinese)  # 心連·情結
# logger.info(res.raw[0].title_english)  # Kokoro Connect
# logger.info(res.raw[0].is_adult)  # False
