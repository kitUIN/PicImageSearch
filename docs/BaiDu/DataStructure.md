# BaiDu

### BaiDu主类说明
```python
baidu = BaiDu(**requests_kwargs)  # 代理设置
```
## 数据返回值列表
!!! note "情境"
    假设我们的代码为
    ```python
    from PicImageSearch import BaiDu

    baidu = BaiDu()
    res = baidu.search('https://i0.hdslb.com/bfs/article/e756dd0a8375a4c30cc0ee3a51c8067157486135.jpg@1524w_856h.webp')
    ```
!!! info 
    - 代理方法见快速开始
    - 数据结构也可以查阅[**源代码**](https://github.com/kitUIN/PicImageSearch/blob/main/PicImageSearch/baidu.py)   

那么以上面的`res`为例

|变量              |   内容             |  类型  |
|----              | ----              | ----  |
|`res.url`|百度识图原网页|str|
|`res.origin`|原始返回值|list|
|`res.raw`|来源结果返回值（具体见下表）|list|
|`res.similar`|相似结果返回值（具体见下表）|list|
|`res.item`|获取所有卡片名(常用来查看卡片)|list|
|`res.cardHeader`|头卡片(卡片例子1)|dict|
|`res.same`|图片来源卡片(卡片例子2)|dict|
|`res.simipic`|相似卡片(卡片例子3)|dict|

!!! tip
    - `res.raw` 存储了所有的返回结果  
    - `res.similar` 储存了所有相似结果
    - `res.cardHeader``res.same``res.simipic`属于卡片，具体取决于百度识图返回的数值
        - `res.baike` 可能返回百度百科识图结果卡片
        - 使用`res.item`查看卡片名称列表
    -  例如`res.raw[0]`内存放了一条搜索结果

=== "res.raw"

    以下列表以`res.raw[0]`为例

    |变量              |   内容             |  类型  |
    |----              | ----              | ----  |
    |`res.raw[0].title`|标题| str|
    |`res.raw[0].page_title`|页面标题| str |
    |`res.raw[0].abstract`|说明文字| str |
    |`res.raw[0].url`|图片所在网页地址|str|
    |`res.raw[0].image_src`|图片地址|str|
    |`res.raw[0].img`|其他图片地址列表|list|

    !!! warning "注意"
        - `res.raw[0].img`可能内容为空

=== "res.similar"
    
    以下列表以`res.similar[0]`为例
    
    |变量              |   内容             |  类型  |
    |----              | ----              | ----  |
    |`res.similar[0]['titles_url']`|标题| str|
    |`res.similar[0]['titles']`|页面标题| str |
    |`res.similar[0]['abstractSrc']`|(用处不大)| int |
    |`res.similar[0]['imgs_url']`|图片所在网页地址|str|
    |`res.similar[0]['imgs_src']`|图片地址|str|
    |`res.similar[0]['data_src']`|(用处不大，可能为空)|str|
    |`res.similar[0]['image_text_score']`|(用处不大，可能为空)|float|
    |`res.similar[0]['isDeadlink']`|(用处不大，可能为空)| int|
    |`res.similar[0]['keyword_text_score']`|(用处不大，可能为空)| int|
    |`res.similar[0]['rankSrc']`|(用处不大，可能为空)|?|
    |`res.similar[0]['rerank_score']`|(用处不大，可能为空)|float|
    |`res.similar[0]['resultSrc']`|(用处不大，可能为空)|str|
    |`res.similar[0]['simi']`|(用处不大，可能为空)|float|
    |`res.similar[0]['snippets']`|(用处不大，可能为空)|str|
    |`res.similar[0]['srcType']`|(用处不大，可能为空)|int|
