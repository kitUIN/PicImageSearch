# Google

### Google主类说明
```python
google = Google(**requests_kwargs)  # 代理设置
```
## 数据返回值列表
!!! note "情境"
    假设我们的代码为
    ```python
    from PicImageSearch import Google

    google = Google()
    res = google.search("https://media.discordapp.net/attachments/783138508038471701/813452582948306974/hl-18-1-900x1280.png?width=314&height=447")
    ```
!!! info 
    - 代理方法见快速开始
    - 数据结构也可以查阅[**源代码**](https://github.com/kitUIN/PicImageSearch/blob/main/PicImageSearch/google.py)   

那么以上面的`res`为例

|变量              |   内容             |  类型  |
|----              | ----              | ----  |
|`res.origin`|原始返回值|list|
|`res.raw`|结果返回值（具体见下表）|list|

!!! tip
    - `res.raw` 存储了所有的返回结果  
    -  例如`res.raw[2]`内存放了一条搜索结果

!!! help
    - 不建议使用`res.raw[0]`与`res.raw[1]`，因为其内容可能是空的
    - 建议从`res.raw[2]`开始使用

以下列表以`res.raw[1]`为例


|变量              |   内容             |  类型  |
|----              | ----              | ----  |
|`res.raw[2].thumbnail`|缩略图地址| list|
|`res.raw[2].titles`|标题| list |
|`res.raw[2].urls`|地址| list |

