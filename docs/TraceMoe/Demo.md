# Demo
## 示例

```python
from loguru import logger
from PicImageSearch import TraceMoe
_REQUESTS_KWARGS = {
    # 'proxies': {
    #     'https': 'http://127.0.0.1:10809',
    # }
    #如果需要代理
}
tracemoe = TraceMoe(**_REQUESTS_KWARGS)
res = tracemoe.search('https://trace.moe/img/tinted-good.jpg')
#res = tracemoe.search(r'C:/kitUIN/img/tinted-good.jpg')搜索本地图片
logger.info(res.origin)  # 原始数据{'RawDocsCount': 5718114, 'RawDocsSearchTime': 15530, 'ReRankSearchTime': 1167, 'CacheHit': False, 'trial': 1, 'docs': [{'from': 1173.83, 'to': 1174.67, 'anilist_id': 11887, 'at': 1174.5, 'season': '2012-07', 'anime': '心連·情結', 'filename': '[ANK-Raws&NatsuYuki] Kokoro Connect - 05 (BDrip 1280x720 x264 AAC).mp4', 'episode': 5, 'tokenthumb': 'I7RtV-BVFDjvgwgPpUwFKw', 'similarity': 0.9685373563005802, 'title': 'ココロコネクト', 'title_native': 'ココロコネクト', 'title_chinese': '心連·情結', 'title_english': 'Kokoro Connect', 'title_romaji': 'Kokoro Connect', 'mal_id': 11887, 'synonyms': ['Kokoroco'], 'synonyms_chinese': ['戀愛隨意鏈', '戀愛隨意連結', '心靈鏈環', '心靈接觸', '心與心的連結'], 'is_adult': False}, {'from': 504.17, 'to': 505.33, 'anilist_id': 849, 'at': 505.17, 'season': '2006-04', 'anime': '涼宮春日的憂鬱', 'filename': '[philosophy-raws][The Melancholy of Haruhi Suzumiya(2006)][12][BDRIP][x264 AAC][1920X1080].mp4', 'episode': 12, 'tokenthumb': 'WKps5xJjEWzVufWEBrS0wQ', 'similarity': 0.819383329990597, 'title': '涼宮ハルヒの憂鬱', 'title_native': '涼宮ハルヒの憂鬱', 'title_chinese': '涼宮春日的憂鬱', 'title_english': 'The Melancholy of Haruhi Suzumiya', 'title_romaji': 'Suzumiya Haruhi no Yuuutsu', 'mal_id': 849, 'synonyms': [], 'synonyms_chinese': [], 'is_adult': False}, {'from': 505.5, 'to': 506, 'anilist_id': 4382, 'at': 505.5, 'season': '2009-04', 'anime': '涼宮春日的憂鬱', 'filename': '[CASO][Suzumiya_Haruhi_no_Yuuutsu][BDrip][26][BIG5][1280x720][x264_AAC].mp4', 'episode': 26, 'tokenthumb': 'fG-kt2NMVPcNECN2hyfCiw', 'similarity': 0.8162108726224474, 'title': '涼宮ハルヒの憂鬱', 'title_native': '涼宮ハルヒの憂鬱', 'title_chinese': '涼宮春日的憂鬱 2009', 'title_english': 'The Melancholy of Haruhi Suzumiya (2009)', 'title_romaji': 'Suzumiya Haruhi no Yuuutsu (2009)', 'mal_id': 4382, 'synonyms': [], 'synonyms_chinese': [], 'is_adult': False}, {'from': 683.5, 'to': 684.75, 'anilist_id': 21085, 'at': 683.5, 'season': '2015-04', 'anime': '鑽石王牌 第二季', 'filename': '[異域字幕組][鑽石王牌第二季][Ace of Diamond S2][18_93][1280x720][繁體].mp4', 'episode': 18, 'tokenthumb': 'IPw8p_4vzsfDaV5QPhF6Gg', 'similarity': 0.8151590465496535, 'title': 'ダイヤのA～Second Season～', 'title_native': 'ダイヤのA～Second Season～', 'title_chinese': '鑽石王牌 第二季', 'title_english': 'Ace of the Diamond Second Season', 'title_romaji': 'Diamond no Ace: Second Season', 'mal_id': 30230, 'synonyms': ['Daiya no Ace 2'], 'synonyms_chinese': [], 'is_adult': False}, {'from': 287.67, 'to': 287.67, 'anilist_id': 854, 'at': 287.67, 'season': '2006-04', 'anime': 'Soul Link', 'filename': '[HKG][Soul.Link][DVDrip][03][x264_AAC][864x480][30fps].mp4', 'episode': 3, 'tokenthumb': 'sFVpsOy02O2r9Jch3CQpXA', 'similarity': 0.8112364293603003, 'title': 'Soul Link', 'title_native': 'Soul Link', 'title_chinese': 'Soul Link', 'title_english': 'Soul Link', 'title_romaji': 'Soul Link', 'mal_id': 854, 'synonyms': [], 'synonyms_chinese': [], 'is_adult': False}, {'from': 232.42, 'to': 232.42, 'anilist_id': 21237, 'at': 232.42, 'season': '2015-10', 'anime': '神之見習者秘密的心靈蛋', 'filename': '(アニメ) かみさまみならい ヒミツのここたま 第02話.mp4', 'episode': 2, 'tokenthumb': 'zPhpsyIfuQG31RVedQ7Mcw', 'similarity': 0.8110595635963628, 'title': 'かみさまみならい ヒミツのここたま', 'title_native': 'かみさまみならい ヒミツのここたま', 'title_chinese': '神之見習者秘密的心靈蛋', 'title_english': 'Kamisama Minarai: Himitsu no Cocotama', 'title_romaji': 'Kamisama Minarai: Himitsu no Cocotama', 'mal_id': 31044, 'synonyms': [], 'synonyms_chinese': ['見習神仙秘密的心靈', '見習神仙精靈'], 'is_adult': False}, {'from': 814.42, 'to': 814.42, 'anilist_id': 18411, 'at': 814.42, 'season': '2013-10', 'anime': '銀狐', 'filename': '[DMG][Gingitsune][09][720P][BIG5].mp4', 'episode': 9, 'tokenthumb': 'PXOTyZYpFvPqsTT-CoLmQQ', 'similarity': 0.8104846724963615, 'title': 'ぎんぎつね', 'title_native': 'ぎんぎつね', 'title_chinese': '銀狐', 'title_english': 'Gingitsune: Messenger Fox of the Gods', 'title_romaji': 'Gingitsune', 'mal_id': 18411, 'synonyms': ['Silver Fox'], 'synonyms_chinese': [], 'is_adult': False}, {'from': 710.33, 'to': 710.33, 'anilist_id': 1482, 'at': 710.33, 'season': '2006-10', 'anime': '驅魔少年', 'filename': '[MapleSnow][D.Gray-man][029][Jpn_Big5][X264_AAC].mp4', 'episode': 29, 'tokenthumb': '2FbPqrT7_vbQZQuplQfp7Q', 'similarity': 0.8095463898281274, 'title': 'ディー・グレイマン', 'title_native': 'ディー・グレイマン', 'title_chinese': '驅魔少年', 'title_english': 'D.Gray-man', 'title_romaji': 'D.Gray-man', 'mal_id': 1482, 'synonyms': ['D. Gray-man', 'D. Grey-man'], 'synonyms_chinese': ['D·格雷少年'], 'is_adult': False}], 'limit': 9, 'limit_ttl': 60, 'quota': 150, 'quota_ttl': 86400}
logger.info(res.raw)  # [<NormTraceMoe(title='心連·情結', similarity=0.97)>, <NormTraceMoe(title='涼宮春日的憂鬱', similarity=0.82)>, <NormTraceMoe(title='涼宮春日的憂鬱 2009', similarity=0.82)>, <NormTraceMoe(title='鑽石王牌 第二季', similarity=0.82)>, <NormTraceMoe(title='Soul Link', similarity=0.81)>, <NormTraceMoe(title='神之見習者秘密的心靈蛋', similarity=0.81)>, <NormTraceMoe(title='銀狐', similarity=0.81)>, <NormTraceMoe(title='驅魔少年', similarity=0.81)>]
logger.info(res.raw[0])  # <NormTraceMoe(title='心連·情結', similarity=0.97)>
logger.info(res.RawDocsCount)  # 5718114
logger.info(res.RawDocsSearchTime)  # 15530
logger.info(res.ReRankSearchTime)  # 1167
logger.info(res.trial)  # 1
logger.info(res.raw[0].thumbnail)  # https://trace.moe/thumbnail.php?anilist_id=11887&file=%5BANK-Raws%26NatsuYuki%5D%20Kokoro%20Connect%20-%2005%20%28BDrip%201280x720%20x264%20AAC%29.mp4&t=1174.5&token=I7RtV-BVFDjvgwgPpUwFKw
logger.info(res.raw[0].video_thumbnail)  # https://media.trace.moe/video/11887/%5BANK-Raws%26NatsuYuki%5D%20Kokoro%20Connect%20-%2005%20%28BDrip%201280x720%20x264%20AAC%29.mp4?t=1174.5&token=I7RtV-BVFDjvgwgPpUwFKw
logger.info(res.raw[0].similarity)  # 0.9685373563005802
logger.info(res.raw[0].From)  # 1173.83
logger.info(res.raw[0].To)  # 1174.67
logger.info(res.raw[0].at)  # 1174.5
logger.info(res.raw[0].anilist_id)  # 11887
logger.info(res.raw[0].season)  # 2012-07
logger.info(res.raw[0].anime)  # 心連·情結
logger.info(res.raw[0].title)  # ココロコネクト
logger.info(res.raw[0].title_native)  # ココロコネクト
logger.info(res.raw[0].title_chinese)  # 心連·情結
logger.info(res.raw[0].title_english)  # Kokoro Connect
logger.info(res.raw[0].is_adult)  # False
```

!!! info "信息"
    文件位于[test1.py](https://github.com/kitUIN/PicImageSearch/tree/main/test/test1.py) 

!!! success
    程序输出,部分过长数据已省略
    ```bash
    ```