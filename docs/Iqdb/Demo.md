# Demo
## 示例

```python
from loguru import logger
from PicImageSearch import Iqdb
_REQUESTS_KWARGS = {
    # 'proxies': {
    #     'https': 'http://127.0.0.1:10809',
    # }
    # 如果需要代理
}
iqdb = Iqdb()
res = iqdb.search('https://ascii2d.net/thumbnail/b/4/a/e/b4ae7762f6d247e04bba6b925ce5f6d1.jpg')

logger.info(res.raw[0].content)    # Best match
logger.info(res.raw[0].url)        # https://yande.re/post/show/681461
logger.info(res.raw[0].thumbnail)  # http://www.iqdb.org/moe.imouto/2/8/b/28beb871b6b162196cd1e4957a2ce5f5.jpg
logger.info(res.raw[0].similarity) # 95% similarity
logger.info(res.raw[0].size)       # 3938×6276 [Ero]
logger.info(res.raw[0].title)      # Rating: q Score: 8 Tags: bikini_top fate/grand_order hews nipples open_shirt saber_extra see_through swimsuits
```

!!! info "信息"
    文件位于[test4.py](https://github.com/kitUIN/PicImageSearch/tree/main/test/test4.py) 

!!! success
    程序输出,部分过长数据已省略
    ```bash
    2021-03-06 19:11:29.157 | INFO     | __main__:<module>:12 - Best match
    2021-03-06 19:11:29.158 | INFO     | __main__:<module>:13 - https://yande.re/post/show/681461
    2021-03-06 19:11:29.158 | INFO     | __main__:<module>:14 - http://www.iqdb.org/moe.imouto/2/8/b/28beb871b6b162196cd1e4957a2ce5f5.jpg
    2021-03-06 19:11:29.158 | INFO     | __main__:<module>:15 - 95% similarity
    2021-03-06 19:11:29.158 | INFO     | __main__:<module>:16 - 3938×6276 [Ero]
    2021-03-06 19:11:29.158 | INFO     | __main__:<module>:17 - Rating: q Score: 8 Tags: bikini_top fate/grand_order hews nipples open_shirt saber_extra see_through swimsuits
    ```