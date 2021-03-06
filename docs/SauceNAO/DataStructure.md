# SauceNAO

## SauceNAO主类说明
```python
saucenao = SauceNAO(
                 api_key='',        # (str)(必须)用于SauceNAO的访问密钥 默认=None 
                 numres = 5,        # (int)输出数量 默认=5
                 hide = 1,          # (int)结果隐藏控制,无=0，明确返回值(默认)=1，怀疑返回值=2，全部返回值=3
                 minsim = 30,       # (int)控制最小相似度 默认=30
                 output_type = 2,   # (int) 0=正常(默认) html 1=xml api（未实现） 2=json api 默认=2
                 testmode = 0,      # (int)测试模式 0=正常 1=测试 默认=0
                 dbmask = None,     # (int)用于选择要启用的特定索引的掩码 默认=None
                 dbmaski = None,    # (int)用于选择要禁用的特定索引的掩码 默认=None
                 db = 999,          # (int)搜索特定的索引号或全部索引 默认=999
                                    # 索引见https://saucenao.com/tools/examples/api/index_details.txt
                 **requests_kwargs  # 代理设置
            )
```
## 数据返回值列表
!!! note "情境"
    假设我们的代码为
    ```python
    from PicImageSeach import SauceNAO

    saucenao = SauceNAO(api_key='输入你的api key',**_REQUESTS_KWARGS)
    res = saucenao.search('https://cdn.jsdelivr.net/gh/laosepi/setu/pics_original/77702503_p0.jpg')
    ```

!!! info 
    - 代理方法见快速开始
    - 数据结构也可以查阅[**源代码**](https://github.com/kitUIN/PicImageSearch/blob/main/PicImageSearch/saucenao.py)   

那么以上面的`res`为例

|变量                    |   内容            |  类型  |
|----                   | ----              | ----  |
|`res.origin`                |原始返回值          |dict|
|`res.short_remaining`       |每30秒访问额度      |int|
|`res.long_remaining`        |每天访问额度        |int|
|`res.user_id`               |API               |int|
|`res.account_type`          |待补充             |int|
|`res.short_limit`           |待补充             |str|
|`res.long_limit`            |待补充            |str|
|`res.status`                |服务器判断值         |int|
|`res.results_requested`     |数据返回值数量        |int|
|`res.search_depth`         |搜索所涉及的数据库数量|str|
|`res.minimum_similarity`    |最小相似度          |float|
|`res.results_returned`      |数据返回值数量        |int|
|`res.raw`                   |结果返回值（具体见下表）|list|


!!! tip
    - `res.raw` 存储了所有的返回结果  
    -  例如`res.raw[0]`内存放了第一条搜索结果  

以下列表以`res.raw[0]`为例


|变量              |   内容             |  类型  |
|----              | ----              | ----  |
|`res.raw[0].raw`|原始值|dict|
|`res.raw[0].similarity`|相似度| float|
|`res.raw[0].thumbnail`|缩略图地址| str|
|`res.raw[0].index_id`|文件id| int|
|`res.raw[0].index_name`|文件名称| str |
|`res.raw[0].title`|标题| str |
|`res.raw[0].url`|地址| str |
|`res.raw[0].author`|作者| str |
|`res.raw[0].pixiv_id`|pixiv的id（如果有）|str|
|`res.raw[0].member_id`|pixiv的画师id（如果有）|str|


## 数据返回值 实例JSON
<details>
  <summary>←←数据返回值 实例JSON(有点长)</summary>
  
```json
{
  "header": {
    "user_id": 0,
    "account_type": 0,
    "short_limit": "4",
    "long_limit": "100",
    "long_remaining": 99,
    "short_remaining": 3,
    "status": 0,
    "results_requested": 10,
    "index": {
      "0": {
        "status": 0,
        "parent_id": 0,
        "id": 0,
        "results": 1
      },
      "2": {
        "status": 0,
        "parent_id": 2,
        "id": 2,
        "results": 1
      },
      "5": {
        "status": 0,
        "parent_id": 5,
        "id": 5,
        "results": 1
      },
      "51": {
        "status": 0,
        "parent_id": 5,
        "id": 51,
        "results": 1
      },
      "52": {
        "status": 0,
        "parent_id": 5,
        "id": 52,
        "results": 1
      },
      "53": {
        "status": 0,
        "parent_id": 5,
        "id": 53,
        "results": 1
      },
      "6": {
        "status": 0,
        "parent_id": 6,
        "id": 6,
        "results": 1
      },
      "8": {
        "status": 0,
        "parent_id": 8,
        "id": 8,
        "results": 1
      },
      "9": {
        "status": 0,
        "parent_id": 9,
        "id": 9,
        "results": 8
      },
      "10": {
        "status": 0,
        "parent_id": 10,
        "id": 10,
        "results": 1
      },
      "11": {
        "status": 0,
        "parent_id": 11,
        "id": 11,
        "results": 1
      },
      "12": {
        "status": 1,
        "parent_id": 9,
        "id": 12
      },
      "16": {
        "status": 0,
        "parent_id": 16,
        "id": 16,
        "results": 1
      },
      "18": {
        "status": 0,
        "parent_id": 18,
        "id": 18,
        "results": 1
      },
      "19": {
        "status": 0,
        "parent_id": 19,
        "id": 19,
        "results": 1
      },
      "20": {
        "status": 0,
        "parent_id": 20,
        "id": 20,
        "results": 1
      },
      "21": {
        "status": 0,
        "parent_id": 21,
        "id": 21,
        "results": 1
      },
      "211": {
        "status": 0,
        "parent_id": 21,
        "id": 211,
        "results": 1
      },
      "22": {
        "status": 0,
        "parent_id": 22,
        "id": 22,
        "results": 1
      },
      "23": {
        "status": 0,
        "parent_id": 23,
        "id": 23,
        "results": 1
      },
      "24": {
        "status": 0,
        "parent_id": 24,
        "id": 24,
        "results": 1
      },
      "25": {
        "status": 1,
        "parent_id": 9,
        "id": 25
      },
      "26": {
        "status": 1,
        "parent_id": 9,
        "id": 26
      },
      "27": {
        "status": 1,
        "parent_id": 9,
        "id": 27
      },
      "28": {
        "status": 1,
        "parent_id": 9,
        "id": 28
      },
      "29": {
        "status": 1,
        "parent_id": 9,
        "id": 29
      },
      "30": {
        "status": 1,
        "parent_id": 9,
        "id": 30
      },
      "31": {
        "status": 0,
        "parent_id": 31,
        "id": 31,
        "results": 1
      },
      "32": {
        "status": 0,
        "parent_id": 32,
        "id": 32,
        "results": 1
      },
      "33": {
        "status": 0,
        "parent_id": 33,
        "id": 33,
        "results": 1
      },
      "34": {
        "status": 0,
        "parent_id": 34,
        "id": 34,
        "results": 1
      },
      "341": {
        "status": 0,
        "parent_id": 341,
        "id": 341,
        "results": 1
      },
      "35": {
        "status": 0,
        "parent_id": 35,
        "id": 35,
        "results": 1
      },
      "36": {
        "status": 0,
        "parent_id": 36,
        "id": 36,
        "results": 1
      },
      "37": {
        "status": 0,
        "parent_id": 37,
        "id": 37,
        "results": 1
      },
      "38": {
        "status": 0,
        "parent_id": 38,
        "id": 38,
        "results": 1
      }
    },
    "search_depth": "128",
    "minimum_similarity": 34.28,
    "query_image_display": "userdata/jQdp26hhZ.jpg.png",
    "query_image": "jQdp26hhZ.jpg",
    "results_returned": 10
  },
  "results": [
    {
      "header": {
        "similarity": "92.22",
        "thumbnail": "https://img1.saucenao.com/res/pixiv/7770/77702503_p0_master1200.jpg?auth\u003dpJmiu8qNI1z2fLBAlAsx7A\u0026exp\u003d1604748473",
        "index_id": 5,
        "index_name": "Index #5: Pixiv Images - 77702503_p0_master1200.jpg"
      },
      "data": {
        "ext_urls": [
          "https://www.pixiv.net/member_illust.php?mode\u003dmedium\u0026illust_id\u003d77702503"
        ],
        "title": "MDR♡",
        "pixiv_id": 77702503,
        "member_name": "CeNanGam",
        "member_id": 4089680
      }
    },
    {
      "header": {
        "similarity": "91.8",
        "thumbnail": "https://img3.saucenao.com/booru/5/0/50430189318ee7163a0ee8219cbaf01e_0.jpg",
        "index_id": 9,
        "index_name": "Index #9: Danbooru - 50430189318ee7163a0ee8219cbaf01e_0.jpg"
      },
      "data": {
        "ext_urls": [
          "https://danbooru.donmai.us/post/show/3679849",
          "https://gelbooru.com/index.php?page\u003dpost\u0026s\u003dview\u0026id\u003d4989243"
        ],
        "danbooru_id": 3679849,
        "gelbooru_id": 4989243,
        "creator": "cenangam",
        "material": "girls frontline",
        "characters": "mdr (girls frontline)",
        "source": "https://i.pximg.net/img-original/img/2019/11/08/00/00/12/77702503"
      }
    },
    {
      "header": {
        "similarity": "92.02",
        "thumbnail": "https://img3.saucenao.com/ehentai/ef/89/ef898d3fb9147c93da40e1f766125cb7bc7dd035.jpg",
        "index_id": 38,
        "index_name": "Index #38: H-Misc (E-Hentai) - ef898d3fb9147c93da40e1f766125cb7bc7dd035.jpg"
      },
      "data": {
        "source": "Artist || CeNanGam",
        "creator": [
          "cenangam"
        ],
        "eng_name": "Artist || CeNanGam",
        "jp_name": "アーティスト || 캐난감"
      }
    },
    {
      "header": {
        "similarity": "44.49",
        "thumbnail": "https://img3.saucenao.com/dA2/82335/823358225.jpg",
        "index_id": 34,
        "index_name": "Index #34: deviantArt2 - 823358225.jpg"
      },
      "data": {
        "ext_urls": [
          "https://deviantart.com/view/823358225"
        ],
        "title": "[ YUK ] Render Anime",
        "da_id": 823358225,
        "author_name": "SAYA-Team",
        "author_url": "https://www.deviantart.com/saya-team"
      }
    },
    {
      "header": {
        "similarity": "41.28",
        "thumbnail": "https://img3.saucenao.com/booru/c/5/c58390b1d6f795ffd1748fcce1bcdd27_0.jpg",
        "index_id": 9,
        "index_name": "Index #9: Danbooru - c58390b1d6f795ffd1748fcce1bcdd27_0.jpg"
      },
      "data": {
        "ext_urls": [
          "https://danbooru.donmai.us/post/show/3679850",
          "https://gelbooru.com/index.php?page\u003dpost\u0026s\u003dview\u0026id\u003d4989242"
        ],
        "danbooru_id": 3679850,
        "gelbooru_id": 4989242,
        "creator": "cenangam",
        "material": "girls frontline",
        "characters": "mdr (girls frontline)",
        "source": "https://i.pximg.net/img-original/img/2019/11/08/00/00/12/77702503"
      }
    },
    {
      "header": {
        "similarity": "33.28",
        "thumbnail": "https://img3.saucenao.com/dA/35722/357220372.jpg",
        "index_id": 34,
        "index_name": "Index #34: deviantArt - 357220372.jpg"
      },
      "data": {
        "ext_urls": [
          "https://deviantart.com/view/357220372"
        ],
        "title": "Joker2",
        "da_id": 357220372,
        "author_name": "shaheerjackal",
        "author_url": "http://shaheerjackal.deviantart.com"
      }
    },
    {
      "header": {
        "similarity": "32.57",
        "thumbnail": "https://img1.saucenao.com/res/pixiv/6034/60346368_p0_master1200.jpg?auth\u003dQrXOCKHI0Rm6ozrAuA7vTA\u0026exp\u003d1604748473",
        "index_id": 5,
        "index_name": "Index #5: Pixiv Images - 60346368_p0_master1200.jpg"
      },
      "data": {
        "ext_urls": [
          "https://www.pixiv.net/member_illust.php?mode\u003dmedium\u0026illust_id\u003d60346368"
        ],
        "title": "DIABOLIK LOVERS LOST EDEN",
        "pixiv_id": 60346368,
        "member_name": "SHiNO",
        "member_id": 15625138
      }
    },
    {
      "header": {
        "similarity": "32.32",
        "thumbnail": "https://img1.saucenao.com/res/seiga_illust/760/7609098.jpg?auth\u003dvJJoGbt5iyWCUiEtFsVS2g\u0026exp\u003d1604748473",
        "index_id": 8,
        "index_name": "Index #8: Nico Nico Seiga - 7609098.jpg"
      },
      "data": {
        "ext_urls": [
          "https://seiga.nicovideo.jp/seiga/im7609098"
        ],
        "title": "壁ドン",
        "seiga_id": 7609098,
        "member_name": "団子",
        "member_id": 5700561
      }
    },
    {
      "header": {
        "similarity": "31.73",
        "thumbnail": "https://img1.saucenao.com/res/pixiv/5536/manga/55365819_p14.jpg?auth\u003dBAggfQ2XuGIqqL40_QyK7g\u0026exp\u003d1604748473",
        "index_id": 5,
        "index_name": "Index #5: Pixiv Images - 55365819_p14.jpg"
      },
      "data": {
        "ext_urls": [
          "https://www.pixiv.net/member_illust.php?mode\u003dmedium\u0026illust_id\u003d55365819"
        ],
        "title": "北国詰め合わせ",
        "pixiv_id": 55365819,
        "member_name": "どーなむろぷ",
        "member_id": 5525947
      }
    },
    {
      "header": {
        "similarity": "31.40",
        "thumbnail": "https://img1.saucenao.com/res/nijie/35/354924.jpg?auth\u003dCShkDag4xnd1ShdEc-2EPA\u0026exp\u003d1604748473",
        "index_id": 11,
        "index_name": "Index #11: Nijie Images - 354924.jpg"
      },
      "data": {
        "ext_urls": [
          "https://nijie.info/view.php?id\u003d354924"
        ],
        "title": "尊姦",
        "nijie_id": 354924,
        "member_name": "コロ太助",
        "member_id": 1449
      }
    }
  ]
}
```
</details>
