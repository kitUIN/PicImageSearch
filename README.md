# PicImageSearch
![release](https://img.shields.io/github/v/release/kitUIN/PicImageSearch)
![issues](https://img.shields.io/github/issues/kitUIN/PicImageSearch)
![stars](https://img.shields.io/github/stars/kitUIN/PicImageSearch)
![forks](https://img.shields.io/github/forks/kitUIN/PicImageSearch)  

聚合整合图片识别api,用于以图搜源(以图搜图，以图搜番)，支持SauceNAO,tracemoe,iqdb,ascii2d,google(谷歌识图),baidu(百度识图)等
# [文档](https://kitUIN.github.io/wiki/picimagesearch/)

## 支持
- [x] [SauceNAO](https://saucenao.com/)
- [x] [TraceMoe](https://trace.moe/) (6月30日更新新的api)
- [x] [Iqdb](http://iqdb.org/)
- [x] [Ascii2D](https://ascii2d.net/)
- [x] [Google谷歌识图](https://www.google.com/imghp)  
- [x] [BaiDu百度识图](https://graph.baidu.com/)
- [x] 异步
## 关于异步用法
使用方法相似且较为简单  
不懂异步的请百度学习异步后再使用  
详细见测试文件夹内异步测试文件  
```python 
async with NetWork() as client:  # 可以设置代理 NetWork(proxy='http://127.0.0.1:10809')
   saucenao = AsyncSauceNAO(client=client)  # client不能少
   res = await saucenao.search('https://pixiv.cat/77702503-1.jpg')
    # 下面操作与同步方法一致
```
### 安装
- 此包需要 Python 3.6 或更新版本。
- `pip install PicImageSearch`
- 或者
- `pip install PicImageSearch -i https://pypi.tuna.tsinghua.edu.cn/simple`

