# 开始

## 例子
!!! 例子

    === "使用代理"

        ```python
        from PicImageSearch import BaiDu

        _REQUESTS_KWARGS = {
             'proxies': {
                 'https': 'http://127.0.0.1:10809',
             }
        }
        baidu = BaiDu(**_REQUESTS_KWARGS)
        res = baidu.search("https://media.discordapp.net/attachments/783138508038471701/813452582948306974/hl-18-1-900x1280.png?width=314&height=447")
        ```

    === "不使用代理"

        ```python
        from PicImageSearch import BaiDu

        baidu = BaiDu()
        res = baidu.search("https://media.discordapp.net/attachments/783138508038471701/813452582948306974/hl-18-1-900x1280.png?width=314&height=447")
        ```


## 搜索图片
```python
from PicImageSearch import BaiDu

baidu = BaiDu()

```
=== "网络图片"
    ```python
    res = baidu.search('https://pixiv.cat/77702503-1.jpg')
    ```
=== "本地图片"
    ```python
    res = baidu.search(r'C:/kitUIN/img/tinted-good.jpg')
    ```



