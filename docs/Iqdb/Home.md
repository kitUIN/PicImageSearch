# 开始

## 例子
!!! 例子

    === "使用代理"

        ```python
        from PicImageSearch import Iqdb

        _REQUESTS_KWARGS = {
             'proxies': {
                 'https': 'http://127.0.0.1:10809',
             }
        }
        iqdb = Iqdb(**_REQUESTS_KWARGS)
        res = iqdb.search('https://pixiv.cat/77702503-1.jpg')
        ```

    === "不使用代理"

        ```python
        from PicImageSearch import Iqdb

        iqdb = Iqdb()
        res = iqdb.search('https://pixiv.cat/77702503-1.jpg')
        ```


## 搜索图片
```python
from PicImageSearch import Iqdb

iqdb = Iqdb()
```
=== "网络图片"
    ```python
    res = iqdb.search('https://ascii2d.net/thumbnail/b/4/a/e/b4ae7762f6d247e04bba6b925ce5f6d1.jpg')
    ```
=== "本地图片"
    ```python
    res = ascii2d.search(r'C:/kitUIN/img/tinted-good.jpg')
    ```

## 搜索图片 3d

```python
from PicImageSearch import Iqdb

iqdb = Iqdb()
```
=== "网络图片"
    ```python
    res = iqdb.search_3d('https://ascii2d.net/thumbnail/b/4/a/e/b4ae7762f6d247e04bba6b925ce5f6d1.jpg')
    ```
=== "本地图片"
    ```python
    res = iqdb.search_3d(r'C:/kitUIN/img/tinted-good.jpg')
    ```


## 异步用法
!!! todo
    - 暂未完成

