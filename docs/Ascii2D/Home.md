# 开始

## 例子
!!! 例子

    === "使用代理"

        ```python
        from PicImageSearch import Ascii2D

        _REQUESTS_KWARGS = {
             'proxies': {
                 'https': 'http://127.0.0.1:10809',
             }
        }
        ascii2d = Ascii2D(**_REQUESTS_KWARGS)
        res = ascii2d.search('https://pixiv.cat/77702503-1.jpg')
        ```

    === "不使用代理"

        ```python
        from PicImageSearch import Ascii2D

        ascii2d = Ascii2D()
        res = ascii2d.search('https://pixiv.cat/77702503-1.jpg')
        ```

!!! warning "注意事项"
    - 不建议使用`res.raw[0]`，因为其内容可能是空的
    - 建议从`res.raw[1]`开始使用  

## 搜索图片
```python
from PicImageSearch import Ascii2D

ascii2d = Ascii2D()
        
```
=== "网络图片"
    ```python
    res = ascii2d.search('https://pixiv.cat/77702503-1.jpg')
    ```
=== "本地图片"
    ```python
    res = ascii2d.search(r'C:/kitUIN/img/tinted-good.jpg')
    ```

!!! help "关于返回结果"
    - 不建议使用`res.raw[0]`，因为其内容可能是空的
    - 建议从`res.raw[1]`开始使用

## 异步用法
!!! todo
    - 暂未完成

