# Demo
## 示例

```python
from loguru import logger

from PicImageSearch import SauceNAO

_REQUESTS_KWARGS = {
    # 'proxies': {
    #     'https': 'http://127.0.0.1:10809',
    # }
    # 如果需要代理
}
saucenao = SauceNAO(api_key='请输入你的key')
res = saucenao.search('https://pixiv.cat/77702503-1.jpg')
#res = saucenao.search(r'C:/kitUIN/img/tinted-good.jpg') #搜索本地图片
logger.info(res.origin)  # 原始数据
logger.info(res.raw)  #
logger.info(res.raw[0])  #
logger.info(res.long_remaining)  # 99
logger.info(res.short_remaining)  # 3
logger.info(res.raw[0].thumbnail)  # https://img1.saucenao.com/res/pixiv/7770/77702503_p0_master1200.jpg?auth=pJmiu8qNI1z2fLBAlAsx7A&exp=1604748473
logger.info(res.raw[0].similarity)  # 92.22
logger.info(res.raw[0].title)  # MDR♡
logger.info(res.raw[0].author)  # CeNanGam
logger.info(res.raw[0].url)  # https://www.pixiv.net/member_illust.php?mode=medium&illust_id=77702503
logger.info(res.raw[0].pixiv_id)  # 77702503
logger.info(res.raw[0].member_id)  # 4089680
```



!!! info "信息"
    文件位于[test2.py](https://github.com/kitUIN/PicImageSearch/tree/main/test/test2.py) 

!!! success
    程序输出
    ```bash
    2021-03-06 19:07:19.845 | INFO     | __main__:<module>:14 - {'header': {'user_id': '42930', 'account_type': '1', 'short_limit': '6', 'long_limit': '200', 'long_remaining': 189, 'short_remaining': 5, 'status': 0, 'results_requested': 5, 'index': {'0': {'status': 0, 'parent_id': 0, 'id': 0, 'results': 5}, '2': {'status': 0, 'parent_id': 2, 'id': 2, 'results': 5}, '5': {'status': 0, 'parent_id': 5, 'id': 5, 'results': 5}, '51': {'status': 0, 'parent_id': 5, 'id': 51, 'results': 5}, '52': {'status': 0, 'parent_id': 5, 'id': 52, 'results': 5}, '53': {'status': 0, 'parent_id': 5, 'id': 53, 'results': 5}, '6': {'status': 0, 'parent_id': 6, 'id': 6, 'results': 5}, '8': {'status': 0, 'parent_id': 8, 'id': 8, 'results': 5}, '9': {'status': 0, 'parent_id': 9, 'id': 9, 'results': 10}, '10': {'status': 0, 'parent_id': 10, 'id': 10, 'results': 5}, '11': {'status': 0, 'parent_id': 11, 'id': 11, 'results': 5}, '12': {'status': 1, 'parent_id': 9, 'id': 12}, '16': {'status': 0, 'parent_id': 16, 'id': 16, 'results': 5}, '18': {'status': 0, 'parent_id': 18, 'id': 18, 'results': 5}, '19': {'status': 0, 'parent_id': 19, 'id': 19, 'results': 5}, '20': {'status': 0, 'parent_id': 20, 'id': 20, 'results': 5}, '21': {'status': 0, 'parent_id': 21, 'id': 21, 'results': 5}, '211': {'status': 0, 'parent_id': 21, 'id': 211, 'results': 5}, '22': {'status': 0, 'parent_id': 22, 'id': 22, 'results': 5}, '23': {'status': 0, 'parent_id': 23, 'id': 23, 'results': 5}, '24': {'status': 0, 'parent_id': 24, 'id': 24, 'results': 5}, '25': {'status': 1, 'parent_id': 9, 'id': 25}, '26': {'status': 1, 'parent_id': 9, 'id': 26}, '27': {'status': 1, 'parent_id': 9, 'id': 27}, '28': {'status': 1, 'parent_id': 9, 'id': 28}, '29': {'status': 1, 'parent_id': 9, 'id': 29}, '30': {'status': 1, 'parent_id': 9, 'id': 30}, '31': {'status': 0, 'parent_id': 31, 'id': 31, 'results': 5}, '32': {'status': 0, 'parent_id': 32, 'id': 32, 'results': 5}, '33': {'status': 0, 'parent_id': 33, 'id': 33, 'results': 5}, '34': {'status': 0, 'parent_id': 34, 'id': 34, 'results': 5}, '341': {'status': 0, 'parent_id': 341, 'id': 341, 'results': 5}, '35': {'status': 0, 'parent_id': 35, 'id': 35, 'results': 5}, '36': {'status': 0, 'parent_id': 36, 'id': 36, 'results': 5}, '37': {'status': 0, 'parent_id': 37, 'id': 37, 'results': 5}, '38': {'status': 0, 'parent_id': 38, 'id': 38, 'results': 5}, '39': {'status': 0, 'parent_id': 39, 'id': 39, 'results': 5}, '40': {'status': 0, 'parent_id': 40, 'id': 40, 'results': 5}, '41': {'status': 0, 'parent_id': 41, 'id': 41, 'results': 5}, '42': {'status': 0, 'parent_id': 42, 'id': 42, 'results': 5}}, 'search_depth': '128', 'minimum_similarity': 30, 'query_image_display': 'userdata/7vTzfKAb7.jpg.png', 'query_image': '7vTzfKAb7.jpg', 'results_returned': 5}, 'results': [{'header': {'similarity': '92.70', 'thumbnail': 'https://img1.saucenao.com/res/pixiv/8802/manga/88020522_p44.jpg?auth=Y8Tnrq2Rk3tCMJOKXcmYMQ&exp=1615320000', 'index_id': 5, 'index_name': 'Index #5: Pixiv Images - 88020522_p44.jpg', 'dupes': 0}, 'data': {'ext_urls': ['https://www.pixiv.net/member_illust.php?mode=medium&illust_id=88020522'], 'title': 'Third time', 'pixiv_id': 88020522, 'member_name': 'Yud', 'member_id': 45860699}}, {'header': {'similarity': '91.10', 'thumbnail': 'https://img1.saucenao.com/res/pixiv/7956/manga/79567666_p1.jpg?auth=JU3JR0xGwT1OEsqlg1sAZA&exp=1615320000', 'index_id': 5, 'index_name': 'Index #5: Pixiv Images - 79567666_p1.jpg', 'dupes': 0}, 'data': {'ext_urls': ['https://www.pixiv.net/member_illust.php?mode=medium&illust_id=79567666'], 'title': 'anime cute girl', 'pixiv_id': 79567666, 'member_name': 'brine', 'member_id': 41469455}}, {'header': {'similarity': '91.11', 'thumbnail': 'https://img1.saucenao.com/res/pixiv/7816/78161553_p0_master1200.jpg?auth=0IQ4VdUPFZC-zkF-uPtDKw&exp=1615320000', 'index_id': 5, 'index_name': 'Index #5: Pixiv Images - 78161553_p0_master1200.jpg', 'dupes': 0}, 'data': {'ext_urls': ['https://www.pixiv.net/member_illust.php?mode=medium&illust_id=78161553'], 'title': 'Untitled', 'pixiv_id': 78161553, 'member_name': 'kei', 'member_id': 41935327}}, {'header': {'similarity': '92.22', 'thumbnail': 'https://img1.saucenao.com/res/pixiv/7770/77702503_p0_master1200.jpg?auth=1A3pU30M6p3UZK8bZrxsTg&exp=1615320000', 'index_id': 5, 'index_name': 'Index #5: Pixiv Images - 77702503_p0_master1200.jpg', 'dupes': 0}, 'data': {'ext_urls': ['https://www.pixiv.net/member_illust.php?mode=medium&illust_id=77702503'], 'title': 'MDR♡', 'pixiv_id': 77702503, 'member_name': 'CeNanGam', 'member_id': 4089680}}, {'header': {'similarity': '94.39', 'thumbnail': 'https://img3.saucenao.com/booru/5/0/50430189318ee7163a0ee8219cbaf01e_5.jpg?auth=TLLkxq1v-ZToG41AKoWLWg&exp=1615320000', 'index_id': 9, 'index_name': 'Index #9: Danbooru - 50430189318ee7163a0ee8219cbaf01e_0.jpg', 'dupes': 2}, 'data': {'ext_urls': ['https://danbooru.donmai.us/post/show/3679849', 'https://gelbooru.com/index.php?page=post&s=view&id=4989243', 'https://anime-pictures.net/pictures/view_post/621762'], 'danbooru_id': 3679849, 'gelbooru_id': 4989243, 'anime-pictures_id': 621762, 'creator': 'cenangam', 'material': 'girls frontline', 'characters': 'mdr (girls frontline)', 'source': 'https://i.pximg.net/img-original/img/2019/11/08/00/00/12/77702503'}}]}
    2021-03-06 19:07:19.849 | INFO     | __main__:<module>:15 - [<NormSauce(title='Third time', similarity=92.70)>, <NormSauce(title='anime cute girl', similarity=91.10)>, <NormSauce(title='Untitled', similarity=91.11)>, <NormSauce(title='MDR♡', similarity=92.22)>, <NormSauce(title='girls frontline', similarity=94.39)>]
    2021-03-06 19:07:19.849 | INFO     | __main__:<module>:16 - <NormSauce(title='Third time', similarity=92.70)>
    2021-03-06 19:07:19.850 | INFO     | __main__:<module>:17 - 189
    2021-03-06 19:07:19.850 | INFO     | __main__:<module>:18 - 5
    2021-03-06 19:07:19.851 | INFO     | __main__:<module>:19 - https://img1.saucenao.com/res/pixiv/8802/manga/88020522_p44.jpg?auth=Y8Tnrq2Rk3tCMJOKXcmYMQ&exp=1615320000
    2021-03-06 19:07:19.851 | INFO     | __main__:<module>:20 - 92.7
    2021-03-06 19:07:19.852 | INFO     | __main__:<module>:21 - Third time
    2021-03-06 19:07:19.852 | INFO     | __main__:<module>:22 - Yud
    2021-03-06 19:07:19.853 | INFO     | __main__:<module>:23 - https://www.pixiv.net/member_illust.php?mode=medium&illust_id=88020522
    2021-03-06 19:07:19.853 | INFO     | __main__:<module>:24 - 88020522
    2021-03-06 19:07:19.854 | INFO     | __main__:<module>:25 - 45860699
    ```