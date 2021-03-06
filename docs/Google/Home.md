# 开始

## 例子
!!! 例子

    === "使用代理"

        ```python
        from PicImageSearch import Google

        _REQUESTS_KWARGS = {
             'proxies': {
                 'https': 'http://127.0.0.1:10809',
             }
        }
        google = Google(**_REQUESTS_KWARGS)
        res = google.search("https://media.discordapp.net/attachments/783138508038471701/813452582948306974/hl-18-1-900x1280.png?width=314&height=447")
        ```

    === "不使用代理"

        ```python
        from PicImageSearch import Google

        google = Google()
        res = google.search("https://media.discordapp.net/attachments/783138508038471701/813452582948306974/hl-18-1-900x1280.png?width=314&height=447")
        ```

!!! warning "注意事项"
    - 不建议使用`res.raw[0]``res.raw[1]`，因为其内容可能是空的
    - 建议从`res.raw[2]`开始使用  

## 搜索图片
```python
from PicImageSearch import Google

google = Google()

```
=== "网络图片"
    ```python
    res = ascii2d.search('https://pixiv.cat/77702503-1.jpg')
    ```
=== "本地图片"
    ```python
    res = google.search("https://media.discordapp.net/attachments/783138508038471701/813452582948306974/hl-18-1-900x1280.png?width=314&height=447")
    ```

!!! help "关于返回结果"
    - 不建议使用`res.raw[0]``res.raw[1]`，因为其内容可能是空的
    - 建议从`res.raw[2]`开始使用  

## 异步用法
!!! todo
    - 暂未完成

