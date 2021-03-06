# 开始

## 例子
!!! 例子

    === "使用代理"

        ```python
        from PicImageSeach import SauceNAO

        _REQUESTS_KWARGS = {
             'proxies': {
                 'https': 'http://127.0.0.1:10809',
             }
        }
        saucenao = SauceNAO(api_key='输入你的api key',**_REQUESTS_KWARGS)
        res = saucenao.search('https://trace.moe/img/tinted-good.jpg')
        ```

    === "不使用代理"

        ```python
        from PicImageSeach import SauceNAO

        saucenao = SauceNAO(api_key='输入你的api key')
        res = saucenao.search('https://trace.moe/img/tinted-good.jpg')
        ```

!!! warning "注意事项"
    - 若是网络不好，则需要使用魔法上网访问[SauceNAO](https://saucenao.com/)
    - 必须使用`api_key`:material-check-circle:[前去申请](https://saucenao.com/user.php?page=search-api) :material-link:

## 搜索图片
```python
from PicImageSeach.saucenao import SauceNAO

saucenao = SauceNAO(api_key='输入你的api key',**_REQUESTS_KWARGS)
```
=== "网络图片"
    ```python
    res = saucenao.search('https://trace.moe/img/tinted-good.jpg')
    ```
=== "本地图片"
    ```python
    res = saucenao.search(r'C:/kitUIN/img/tinted-good.jpg')
    ```
## 异步用法
!!! todo
    - 暂未完成

## 下载缩略图
- 此为附加功能:material-file-download:
```python
from PicImageSeach import SauceNAO

saucenao = SauceNAO(api='输入你的api key')
res = saucenao.search('https://trace.moe/img/tinted-good.jpg')
res.raw[0].download_thumbnail(filename='文件名')
```