# Demo
## 示例

```python
from PicImageSearch import BaiDu
from loguru import logger

baidu = BaiDu()
res = baidu.search('https://i0.hdslb.com/bfs/article/e756dd0a8375a4c30cc0ee3a51c8067157486135.jpg@1524w_856h.webp')
logger.info(res.item)
logger.info(res.raw[0].title)
logger.info(res.raw[0].page_title)
logger.info(res.raw[0].abstract)
logger.info(res.raw[0].url)
logger.info(res.raw[0].image_src)
```

!!! info "信息"
    文件位于[test6.py](https://github.com/kitUIN/PicImageSearch/tree/main/test/test6.py)

!!! success
    程序输出,部分过长数据已省略
    ```shell
    2021-03-13 22:16:19.199 | INFO     | __main__:<module>:6 - ['cardHeader', 'similar', 'simipic']
    2021-03-13 22:16:19.199 | INFO     | __main__:<module>:7 - 哔哩哔哩2233娘－堆糖，美好生活研究所
    2021-03-13 22:16:19.200 | INFO     | __main__:<module>:8 - 哔哩哔哩2233娘－堆糖，美好生活研究所
    2021-03-13 22:16:19.200 | INFO     | __main__:<module>:9 - ['2018年9月23日 15:57   关注  评论 收藏']
    2021-03-13 22:16:19.200 | INFO     | __main__:<module>:10 - https://graph.baidu.com/api/proxy?mroute=redirect&sec=1615644979048&seckey=8b90708a30&u=http%3A%2F%2Fwww-beta1.duitang.com%2Fblog%2F%3Fid%3D996666943
    2021-03-13 22:16:19.200 | INFO     | __main__:<module>:11 - https://ss2.baidu.com/6ON1bjeh1BF3odCf/it/u=3838910805,2766590892&fm=27&gp=0.jpg
    ```    
