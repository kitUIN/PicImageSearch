# PicImageSearch
![release](https://img.shields.io/github/v/release/kitUIN/PicImageSearch)
![issues](https://img.shields.io/github/issues/kitUIN/PicImageSearch)
![stars](https://img.shields.io/github/stars/kitUIN/PicImageSearch)
![forks](https://img.shields.io/github/forks/kitUIN/PicImageSearch)  
聚合识图引擎  
整合图片识别api,用于以图搜源(以图搜图，以图搜番)，支持SauceNAO,tracemoe,iqdb,ascii2d,google(谷歌识图),baidu(百度识图),E-Hantai,ExHantai识图
# [文档](https://www.kituin.fun/wiki/picimagesearch/)

## 支持
- [x] [SauceNAO](https://saucenao.com/)
- [x] [TraceMoe](https://trace.moe/)
- [x] [Iqdb](http://iqdb.org/)
- [x] [Ascii2D](https://ascii2d.net/)
- [x] [Google谷歌识图](https://www.google.com/imghp)  
- [x] [BaiDu百度识图](https://graph.baidu.com/)
- [x] [E-Hantai](https://e-hentai.org/)  
- [x] [ExHantai](https://exhentai.org/)  
- [x] 同步/异步
## 简要说明

详细见[文档](https://www.kituin.fun/wiki/picimagesearch/) 或者[`demo`](https://github.com/kitUIN/PicImageSearch/tree/main/demo)  
`同步`请使用`from PicImageSearch.sync import ...`导入  
`异步`请使用`from PicImageSearch import Network,...`导入  
**推荐使用异步**  

## 简单示例
```python
from loguru import logger
from PicImageSearch.sync import SauceNAO

saucenao = SauceNAO()
res = saucenao.search('https://pixiv.cat/77702503-1.jpg')
# res = saucenao.search(r'C:/kitUIN/img/tinted-good.jpg') #搜索本地图片
logger.info(res.origin)  # 原始数据
logger.info(res.raw)  #
logger.info(res.raw[0])  #
logger.info(res.long_remaining)  # 99
logger.info(res.short_remaining)  # 3
logger.info(res.raw[0].thumbnail)  # 缩略图
logger.info(res.raw[0].similarity)  # 相似度
logger.info(res.raw[0].title)  # 标题
logger.info(res.raw[0].author)  # 作者
logger.info(res.raw[0].url)
```

```python
from PicImageSearch import SauceNAO, Network

async with Network() as client:  # 可以设置代理 Network(proxies='http://127.0.0.1:10809')
    saucenao = SauceNAO(client=client)  # client不能少
    res = await saucenao.search('https://pixiv.cat/77702503-1.jpg')
    # 下面操作与同步方法一致
```
### 安装
- 此包需要 Python 3.6 或更新版本。
- `pip install PicImageSearch`
- 或者
- `pip install PicImageSearch -i https://pypi.tuna.tsinghua.edu.cn/simple`

