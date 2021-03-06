# Iqdb

### Iqdb主类说明
```python
iqdb = Iqdb(**requests_kwargs)  # 代理设置
```

## 数据返回值列表
!!! note "情境"
    假设我们的代码为
    ```python
    from PicImageSearch import Iqdb

    iqdb = Iqdb()
    res = iqdb.search('https://ascii2d.net/thumbnail/b/4/a/e/b4ae7762f6d247e04bba6b925ce5f6d1.jpg')
    ```
!!! info 
    - 代理方法见快速开始
    - 数据结构也可以查阅[**源代码**](https://github.com/kitUIN/PicImageSearch/blob/main/PicImageSearch/iqdb.py)   

那么以上面的`res`为例

|变量              |   内容             |  类型  |
|----              | ----              | ----  |
|`res.origin`|原始返回值|list|
|`res.raw`|结果返回值（具体见下表）|list|

!!! tip
    - `res.raw` 存储了所有的返回结果  
    -  例如`res.raw[0]`内存放了第一条搜索结果

以下列表以`res.raw[0]`为例


|变量              |   内容             |  类型  |
|----              | ----              | ----  |
|`res.raw[0].similarity`|相似值|str|
|`res.raw[0].thumbnail`|缩略图地址| str|
|`res.raw[0].title`|标题| str |
|`res.raw[0].url`|地址| str |
|`res.raw[0].content`|备注| str |
|`res.raw[0].size`|原图长宽大小|str|

