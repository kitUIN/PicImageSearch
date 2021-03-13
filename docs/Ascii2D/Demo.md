# Demo
## 示例

```python
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
```

!!! info "信息"
    文件位于[test3.py](https://github.com/kitUIN/PicImageSearch/tree/main/test/test3.py) 

!!! help
    - 不建议使用`res.raw[0]`，因为其内容可能是空的
    - 建议从`res.raw[1]`开始使用

!!! success
    程序输出,部分过长数据已省略
    ```shell
    2021-03-06 18:58:21.508 | INFO     | __main__:<module>:8 - [<div class="row item-box">.......
    2021-03-06 18:58:21.533 | INFO     | __main__:<module>:9 - [<NormAscii2D(title=[], authors=[],mark=[])>, <NormAscii2D(title=['MDR♡'], authors=['CeNanGam'],mark=['\npixiv\n'])>, <NormAscii2D(title=['Untitled'], authors=['Kei春菜'],mark=['\npixiv\n'])>, <NormAscii2D(title=['細川まとめ'], authors=['足袋'],mark=['\npixiv\n'])>, <NormAscii2D(title=['ついろぐ(1月14日～3月20日)'], authors=['Pova*'],mark=['\npixiv\n'])>, <NormAscii2D(title=['2019.01.06'], authors=['aengdohwa'],mark=['twitter'])>, <NormAscii2D(title=['2018.05.23'], authors=['aengdohwa'],mark=['twitter'])>, <NormAscii2D(title=['一松'], authors=['スティ'],mark=['\npixiv\n'])>, <NormAscii2D(title=['2020.02.20'], authors=['ame_ame05'],mark=['twitter'])>, <NormAscii2D(title=['2020.09.12'], authors=['waru_geli'],mark=['twitter'])>, <NormAscii2D(title=['Elsa'], authors=['Waru-Geli'],mark=['\npixiv\n'])>, <NormAscii2D(title=['无题'], authors=['Zzb'],mark=['\npixiv\n'])>, <NormAscii2D(title=['一左馬かわいいな'], authors=['DA犬'],mark=['\npixiv\n'])>, <NormAscii2D(title=['宗みかLOG'], authors=['本田あき'],mark=['\npixiv\n'])>, <NormAscii2D(title=['呪術ろぐ'], authors=['杏'],mark=['\npixiv\n'])>, <NormAscii2D(title=['落書きまとめ'], authors=['鳩太郎'],mark=['\npixiv\n'])>, <NormAscii2D(title=['秀零ろぐ'], authors=['yunga=docson'],mark=['\npixiv\n'])>, <NormAscii2D(title=['無題'], authors=['Wyatt.W'],mark=['\npixiv\n'])>, <NormAscii2D(title=['【PFFK】人形師の暗躍【骸ヶ原の挟撃】'], authors=['Aria＠ままん'],mark=['\npixiv\n'])>, <NormAscii2D(title=['サリアマ'], authors=['紅葉狩り'],mark=['\npixiv\n'])>, <NormAscii2D(title=['無題'], authors=['NEE@みつきやよい'],mark=['\npixiv\n'])>]
    2021-03-06 18:58:21.534 | INFO     | __main__:<module>:10 - <NormAscii2D(title=['MDR♡'], authors=['CeNanGam'],mark=['\npixiv\n'])>
    2021-03-06 18:58:21.534 | INFO     | __main__:<module>:11 - https://ascii2d.net/thumbnail/5/0/4/3/50430189318ee7163a0ee8219cbaf01e.jpg
    2021-03-06 18:58:21.534 | INFO     | __main__:<module>:12 - MDR♡
    2021-03-06 18:58:21.535 | INFO     | __main__:<module>:13 - CeNanGam
    2021-03-06 18:58:21.535 | INFO     | __main__:<module>:14 - https://www.pixiv.net/artworks/77702503
    2021-03-06 18:58:21.535 | INFO     | __main__:<module>:15 - 919x1300 JPEG 1002.6KB
    ```