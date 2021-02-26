from loguru import logger

from PicImageSearch import Google

google = Google()
res = google.search("https://media.discordapp.net/attachments/783138508038471701/813452582948306974/hl-18-1-900x1280.png?width=314&height=447")
#res = google.search(r'C:/kitUIN/img/tinted-good.jpg')  # Search Image URL or path
logger.info(res.origin)  # Original Data
logger.info(res.raw)  # Raw Data
# Should start from index 2, because from there is matching image
logger.info(res.raw[2])  # <NormGoogle(title=["The Strongest Dull Prince's Secret Battle for the Throne ..."], urls=['https://kiryuu.co/the-strongest-dull-princes-secret-battle-for-the-throne-chapter-3-bahasa-indonesia/'], thumbnail=['No directable url'])>
logger.info(res.raw[2].thumbnail[0])  # No directable url
logger.info(res.raw[2].titles[0])  # The Strongest Dull Prince's Secret Battle for the Throne ...
logger.info(res.raw[2].urls[0])  # https://kiryuu.co/the-strongest-dull-princes-secret-battle-for-the-throne-chapter-3-bahasa-indonesia/