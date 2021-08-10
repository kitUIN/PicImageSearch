import requests


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

    def download_thumbnail(self, filename='thumbnail.png'):  # 缩略图生成
        with requests.get(self.thumbnail, stream=True) as resp:
            with open(filename, 'wb') as fd:
                for chunk in resp.iter_content():
                    fd.write(chunk)

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
        return f'<NormSauceNAO(title={repr(self.title)}, similarity={self.similarity:.2f})>'


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
        return (f'<SauceNAOResponse(count={repr(len(self.raw))}, long_remaining={repr(self.long_remaining)}, '
                f'short_remaining={repr(self.short_remaining)})>')

