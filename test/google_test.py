from loguru import logger
from PicImageSearch import Google

google = Google()
res = google.search(
    "https://media.discordapp.net/attachments/783138508038471701/813452582948306974/hl-18-1-900x1280.png?width=314&height=447"
)
# res = google.search(r'C:/kitUIN/img/tinted-good.jpg')  # Search Image URL or path
logger.info(res.origin)  # Original Data

# Should start from index 2, because from there is matching image
logger.info(
    res.raw[4]
)  # <NormGoogle(title=["The Strongest Dull Prince's Secret Battle for the Throne ..."], urls=['https://kiryuu.co/the-strongest-dull-princes-secret-battle-for-the-throne-chapter-3-bahasa-indonesia/'], thumbnail=['No detectable url'])>
logger.info(res.raw[4].thumbnail)  # No detectable url
logger.info(
    res.raw[4].title
)  # The Strongest Dull Prince's Secret Battle for the Throne ...
logger.info(
    res.raw[4].url
)  # https://kiryuu.co/the-strongest-dull-princes-secret-battle-for-the-throne-chapter-3-bahasa-indonesia/
logger.info(res.page)
res2 = google.goto_page(res.get_page_url(2), 2)
logger.info(res2.raw[2])
logger.info(res2.raw[2].thumbnail)
logger.info(res2.raw[2].title)
logger.info(res2.raw[2].url)
