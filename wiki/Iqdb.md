# Iqdb
## 如何开始
```
(测试文件在这里https://github.com/kitUIN/PicImageSearch/tree/main/test/test4.py)
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
#result = ascii2d.search(r'C:/kitUIN/img/tinted-good.jpg')搜索本地图片
logger.info(result.origin)  # 原始数据
res = result.raw[0]
logger.info(res.content)    # Best match
logger.info(res.url)        # https://yande.re/post/show/681461
logger.info(res.thumbnail)  # http://www.iqdb.org/moe.imouto/2/8/b/28beb871b6b162196cd1e4957a2ce5f5.jpg
logger.info(res.similarity) # 95% similarity
logger.info(res.size)       # 3938×6276 [Ero]
logger.info(res.title)      # Rating: q Score: 8 Tags: bikini_top fate/grand_order hews nipples open_shirt saber_extra see_through swimsuits

```
### Ascii2D主类说明
```
    iqdb = Iqdb(
                **requests_kwargs  # 代理设置
    )
```
## 数据返回值列表
PS：可以去看看[**源代码**](https://github.com/kitUIN/PicImageSearch/blob/main/PicImageSearch/iqdb.py)   
以上面的`res`为例  
|变量              |   内容             |  类型  |
|----              | ----              | ----  |
|.origin|原始返回值|bytes|
|.raw|结果返回值（具体见下表）|list|
- `res.raw` 存储了所有的返回结果  
-  例如`res.raw[0]`内存放了第一条搜索结果  
-  以下列表以`res.raw[0]`为例


|变量              |   内容             |  类型  |
|----              | ----              | ----  |
|.similarity|相似值|str|
|.thumbnail|缩略图地址| str|
|.title|标题| str |
|.url|地址| str |
|.content|备注| str |
|.size|原图长宽大小|str|