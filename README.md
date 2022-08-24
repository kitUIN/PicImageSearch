<div align="center">

# PicImageSearch

✨ 聚合识图引擎 用于以图搜源✨
</div>

<p align="center">
  <a href="https://raw.githubusercontent.com/kitUIN/PicImageSearch/master/LICENSE">
    <img src="https://img.shields.io/github/license/kitUIN/PicImageSearch" alt="license">
  </a>
  <a href="https://pypi.python.org/pypi/PicImageSearch">
    <img src="https://img.shields.io/pypi/v/PicImageSearch" alt="pypi">
  </a>
  <img src="https://img.shields.io/badge/python-3.7+-blue" alt="python">
  <a href="https://github.com/kitUIN/PicImageSearch/releases">
    <img src="https://img.shields.io/github/v/release/kitUIN/PicImageSearch" alt="release">
  </a>
  <a href="https://github.com/kitUIN/PicImageSearch/issues">
    <img src="https://img.shields.io/github/issues/kitUIN/PicImageSearch" alt="release">
  </a>
 </p>
<p align="center">
  <a href="https://pic-image-search.kituin.fun/">📖文档</a>
  ·
  <a href="https://github.com/kitUIN/PicImageSearch/issues/new">🐛提交建议</a>
</p>

## 支持

- [x] [SauceNAO](https://saucenao.com/)
- [x] [TraceMoe](https://trace.moe/)
- [x] [Iqdb](http://iqdb.org/)
- [x] [Ascii2D](https://ascii2d.net/)
- [x] [Google谷歌识图](https://www.google.com/imghp)
- [x] [BaiDu百度识图](https://graph.baidu.com/)
- [x] [E-Hentai](https://e-hentai.org/)
- [x] [ExHentai](https://exhentai.org/)
- [x] 同步/异步

## 简要说明

详细见[文档](https://pic-image-search.kituin.fun/) 或者[`demo`](https://github.com/kitUIN/PicImageSearch/tree/main/demo)  
`同步`请使用`from PicImageSearch.sync import ...`导入  
`异步`请使用`from PicImageSearch import Network,...`导入  
**推荐使用异步**  

## 简单示例

```python
from loguru import logger
from PicImageSearch import SauceNAO, Network

async with Network() as client:  # 可以设置代理 Network(proxies='scheme://host:port')
    saucenao = SauceNAO(client=client, api_key="your api key")  # client, api_key 不能少
    url = "https://raw.githubusercontent.com/kitUIN/PicImageSearch/main/demo/images/test01.jpg"
    resp = await saucenao.search(url=url)
    # 搜索本地图片
    # file = "demo/images/test01.jpg"
    # resp = await saucenao.search(file=file)

    logger.info(resp.status_code)  # HTTP 状态码
    # logger.info(resp.origin)  # 原始数据
    logger.info(resp.raw[0].origin)
    logger.info(resp.long_remaining)
    logger.info(resp.short_remaining)
    logger.info(resp.raw[0].thumbnail)
    logger.info(resp.raw[0].similarity)
    logger.info(resp.raw[0].hidden)
    logger.info(resp.raw[0].title)
    logger.info(resp.raw[0].author)
    logger.info(resp.raw[0].url)
    logger.info(resp.raw[0].pixiv_id)
    logger.info(resp.raw[0].member_id)
```

```python
from PicImageSearch.sync import SauceNAO

saucenao = SauceNAO(api_key="your api key")  # api_key 不能少
url = "https://raw.githubusercontent.com/kitUIN/PicImageSearch/main/demo/images/test01.jpg"
resp = saucenao.search(url=url)
# 搜索本地图片
# file = "demo/images/test01.jpg"
# resp = saucenao.search(file=file)
# 下面操作与异步方法一致
```

### 安装

- 此包需要 Python 3.7 或更新版本。
- `pip install PicImageSearch`
- 或者
- `pip install PicImageSearch -i https://pypi.tuna.tsinghua.edu.cn/simple`

## Star History

[![Star History](https://starchart.cc/kitUIN/PicImageSearch.svg)](https://starchart.cc/kitUIN/PicImageSearch)
