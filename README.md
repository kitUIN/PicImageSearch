# PicImageSearch
整合图片识别api,包括SauceNAO,tracemoe,iqdb,ascii2d等
## TODO
- [ ] [SauceNAO]
- [x] [TraceMoe](https://trace.moe/)
- [ ] [iqdb]
- [ ] [ascii2d]
### 安装
- 此包需要 Python 3.6 或更新版本。
- `pip install PicImageSearch`
- 或者
- `pip install PicImageSearch -i https://pypi.tuna.tsinghua.edu.cn/simple`

### 帮助手册目录
  - SauceNAO
  - [TraceMoe](https://github.com/kitUIN/PicImageSearch#tracemoe)
  - iqdb
  - ascii2d
### TraceMoe
#### 如何开始
如果是需要查找的是网络url
```
from PicImageSearch import TraceMoe

tracemoe = TraceMoe()
tracemoe.search('https://trace.moe/img/tinted-good.jpg')

#tracemoe.search(网络地址或本地,是否是本地文件(默认否),搜索限制为特定的 Anilist ID(默认无))

print(tracemoe.raw)
```
如果是需要查找的是本地文件,使用以下语句即可
```
tracemoe.search(r'C:/kitUIN/img/tinted-good.jpg',True)
```

返回值储存在上文`tracemoe`  
详细数据见下表
|变量              |   内容             |  类型  |
|----              | ----                   | ----  |
|.raw              |最匹配项返回结果|dict|
|.raw_all          |总返回|dict|
|.raws             |其他返回|dict|
|.viedo            |视频预览url|str|
|.thumbnail        |缩略图预览url|str|
|.RawDocsCount     |搜索的帧总数|int|
|.RawDocsSearchTime|从数据库检索帧所用的时间|int|
|.ReRankSearchTime |比较帧所用的时间|int|
|.CacheHit         |是否缓存搜索结果|bool|
|.trial            |搜索时间|int|
|.limit            |剩余搜索限制数|int|
|.limit_ttl        |限制重置之前的时间（秒）|int|
|.quota            |剩余搜索配额数|int|
|.quota_ttl        |配额重置之前的时间（秒）|int|
| 以下可作为.raws的值  |                 |     |
|.From             |匹配场景的开始时间|int|
|.to               |匹配场景的结束时间|int|
|.anilist_id       |匹配的[Anilist  ID](https://anilist.co/)|int|
|.at               |匹配场景的确切时间|float|
|.season           |发布时间|str|
|.anime            |番剧名字|str|
|.filename         |找到匹配项的文件名|str|
|.episode          |估计的匹配的番剧的集数|int|
|.tokenthumb       |用于生成预览的token|str|
|.similarity       |相似度，相似性低于 87% 的搜索结果可能是不正确的结果|float|
|.title            |番剧名字|str|
|.title_native     |番剧世界命名|str|
|.title_chinese    |番剧中文命名|str|
|.title_english    |番剧英文命名|str|
|.title_romaji     |番剧罗马命名|str|
|.mal_id           |匹配的[MyAnimelist  ID](https://myanimelist.net/)|int|
|.synonyms         |备用英文标题|str|
|.synonyms_chinese |备用中文标题|str|
|.is_adult         |是否R18|bool|

若是想查看其他搜索返回值可以使用.raws[序号(从0开始)][值(上表)]  
例如`tracemoe.raws[1]['similarity']`查看第2条的相似度

预览图片/视频下载到本地
```
download_image(tracemoe.thumbnail)#下载图片image.png

#download_image(预览图片url)

download_viedo(tracemoe.viedo)#下载视频video.mp4

#download_viedo(预览视频url)

```