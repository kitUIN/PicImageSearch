import requests
import urllib3
from loguru import logger
from requests_toolbelt import MultipartEncoder


class SauceNAONorm:
    def __init__(self, data):
        result_header = data['header']
        result_data = data['data']
        self.raw: dict = data
        self.similarity: float = float(result_header['similarity'])
        self.thumbnail: str = result_header['thumbnail']
        self.index_id: int = result_header['index_id']
        self.index_name: str = result_header['index_name']
        self.title: str = self._get_title(result_data)
        self.url: str = self._get_url(result_data)
        self.author: str = self._get_author(result_data)
        self.pixiv_id: str = self._get_pixiv_id(result_data)
        self.member_id: str = self._get_member_id(result_data)

    @staticmethod
    def _get_title(data):
        if 'title' in data:
            return data['title']
        elif 'eng_name' in data:
            return data['eng_name']
        elif 'material' in data:
            return data['material']
        elif 'source' in data:
            return data['source']
        elif 'created_at' in data:
            return data['created_at']

    @staticmethod
    def _get_url(data):
        if 'ext_urls' in data:
            return data['ext_urls'][0]
        elif 'getchu_id' in data:
            return f'http://www.getchu.com/soft.phtml?id={data["getchu_id"]}'
        return ''

    @staticmethod
    def _get_author(data):
        if 'author' in data:
            return data['author']
        elif 'author_name' in data:
            return data['author_name']
        elif 'member_name' in data:
            return data['member_name']
        elif 'pawoo_user_username' in data:
            return data['pawoo_user_username']
        elif 'company' in data:
            return data['company']
        elif 'creator' in data:
            if isinstance(data['creator'], list):
                return data['creator'][0]
            return data['creator']

    @staticmethod
    def _get_pixiv_id(data):
        if 'pixiv_id' in data:
            return data['pixiv_id']
        else:
            return ''

    @staticmethod
    def _get_member_id(data):
        if 'member_id' in data:
            return data['member_id']
        else:
            return ''

    def __repr__(self):
        return f'<NormSauce(title={repr(self.title)}, similarity={self.similarity:.2f})>'


class SauceNAOResponse:
    def __init__(self, resp):
        self.raw: list = []
        resp_header = resp['header']
        resp_results = resp['results']
        for i in resp_results:
            self.raw.append(SauceNAONorm(i))
        self.origin: dict = resp
        self.short_remaining: int = resp_header['short_remaining']  # 每30秒访问额度
        self.long_remaining: int = resp_header['long_remaining']  # 每天访问额度
        self.user_id: int = resp_header['user_id']
        self.account_type: int = resp_header['account_type']
        self.short_limit: str = resp_header['short_limit']
        self.long_limit: str = resp_header['long_limit']
        self.status: int = resp_header['status']
        self.results_requested: int = resp_header['results_requested']
        self.search_depth: str = resp_header['search_depth']
        self.minimum_similarity: float = resp_header['minimum_similarity']
        self.results_returned: int = resp_header['results_returned']

    def __repr__(self):
        return (f'<SauceResponse(count={repr(len(self.raw))}, long_remaining={repr(self.long_remaining)}, '
                f'short_remaining={repr(self.short_remaining)})>')


class SauceNAO:
    SauceNAOURL = 'https://saucenao.com/search.php'

    def __init__(self,
                 api_key: str = None,
                 *,
                 numres: int = 5,
                 hide: int = 1,
                 minsim: int = 30,
                 output_type: int = 2,
                 testmode: int = 0,
                 dbmask: int = None,
                 dbmaski: int = None,
                 db: int = 999,
                 **requests_kwargs
                 ) -> None:
        """
        :param api_key:(str)用于SauceNAO的访问密钥 (默认=None)
        :param output_type:(int) 0=正常(默认) html 1=xml api（未实现） 2=json api 默认=2
        :param testmode:(int) 测试模式 0=正常 1=测试 (默认=0)
        :param numres:(int)输出数量 (默认=5)
        :param dbmask:(int)用于选择要启用的特定索引的掩码 (默认=None)
        :param dbmaski:(int)用于选择要禁用的特定索引的掩码 (默认=None)
        :param db:(int)搜索特定的索引号或全部索引 (默认=999)，索引见https://saucenao.com/tools/examples/api/index_details.txt
        :param minsim:(int)控制最小相似度 (默认=30)
        :param hide:(int)结果隐藏控制,无=0，明确返回值(默认)=1，怀疑返回值=2，全部返回值=3
        """
        # minsim 控制最小相似度
        self.requests_kwargs = requests_kwargs
        params = dict()
        if api_key is not None:
            params['api_key'] = api_key
        if dbmask is not None:
            params['dbmask'] = dbmask
        if dbmaski is not None:
            params['dbmaski'] = dbmaski
        params['testmode'] = testmode
        params['numres'] = numres
        params['output_type'] = output_type
        params['hide'] = hide
        params['db'] = db
        params['minsim'] = minsim
        self.params = params

    def search(self, url: str):
        params = self.params
        headers = {}
        m = None
        if url[:4] == 'http':  # 网络url
            params['url'] = url
        else:  # 文件
            m = MultipartEncoder(
                fields={
                    'file': ('filename', open(url, 'rb'), "type=multipart/form-data")
                }
            )
            headers = {'Content-Type': m.content_type}
        urllib3.disable_warnings()
        resp = requests.post(self.SauceNAOURL, headers=headers, data=m, params=params, verify=False,
                             **self.requests_kwargs)
        status_code = resp.status_code
        logger.info(status_code)
        data = resp.json()
        return SauceNAOResponse(data)

    @staticmethod
    def download_thumbnail(thumbnail, filename='thumbnail.png'):
        with requests.get(thumbnail, stream=True) as resp:
            with open(filename, 'wb') as fd:
                for chunk in resp.iter_content():
                    fd.write(chunk)
