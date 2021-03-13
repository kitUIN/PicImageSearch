# 开始

## 例子
!!! 例子

    === "使用代理"

        ```python
        from PicImageSearch import TraceMoe

        _REQUESTS_KWARGS = {
             'proxies': {
                 'https': 'http://127.0.0.1:10809',
             }
        }
        tracemoe = TraceMoe(**_REQUESTS_KWARGS)
        res = tracemoe.search('https://trace.moe/img/tinted-good.jpg')
        ```

    === "不使用代理"

        ```python
        from PicImageSearch import TraceMoe

        tracemoe = TraceMoe()
        res = tracemoe.search('https://trace.moe/img/tinted-good.jpg')
        ```



## 搜索图片
```python
from PicImageSearch import TraceMoe
    
tracemoe = TraceMoe()   
```
=== "网络图片"
    ```python
    res = tracemoe.search('https://pixiv.cat/77702503-1.jpg')
    ```
=== "本地图片"
    ```python
    res = tracemoe.search(r'C:/kitUIN/img/tinted-good.jpg')
    ```

## 下载缩略图
- 此为附加功能:material-file-download:
```python
from PicImageSearch import TraceMoe
    
tracemoe = TraceMoe()
res = tracemoe.search('https://trace.moe/img/tinted-good.jpg')
res.raw[0].download_thumbnail(filename='文件名')
```
## 下载预览视频
- 此为附加功能:material-file-download:
```python
from PicImageSearch import TraceMoe
    
tracemoe = TraceMoe()
res = tracemoe.search('https://trace.moe/img/tinted-good.jpg')
res.raw[0].download_video(filename='文件名')
```
