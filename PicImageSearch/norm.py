import json
import re
import requests

from urllib import parse

class Ascii2DNorm:
    URL = 'https://ascii2d.net'

    def __init__(self, data):
        self.thumbnail = ""
        self.detail: str = data[3].small.string
        self.title = ""
        self.authors = ""
        self.url = ""
        self.marks = ""
        self._arrange(data)

    def _arrange(self, data):
        o_url = data[3].find('div', class_="detail-box gray-link").contents
        urls = self._geturls(o_url)
        self.thumbnail = self.URL + data[1].find('img')['src']
        self.url = urls['url']
        self.title = urls['title']
        self.authors = urls['authors']
        self.marks = urls['mark']

    @staticmethod
    def _geturls(data):
        all_urls = {
            'url': "",
            'title': "",
            'authors_urls': "",
            'authors': "",
            'mark': ""
        }

        for x in data:
            if x == '\n':
                continue
            try:
                origin = x.find_all('a')
                all_urls['url'] = origin[0]['href']
                all_urls['title'] = origin[0].string
                all_urls['authors_urls'] = origin[1]['href']
                all_urls['authors'] = origin[1].string
                all_urls['mark'] = x.small.string
            except:
                pass
        return all_urls

    def __repr__(self):
        return f'<NormAscii2D(title={repr(self.title)}, authors={self.authors}, mark={self.marks})>'


class BaiDuNorm:
    def __init__(self, data):
        self.origin: dict = data
        self.page_title: str = data['fromPageTitle']
        self.title: str = data['title'][0]
        self.abstract: str = data['abstract']
        self.image_src: str = data['image_src']
        self.url: str = data['url']
        self.img = list()
        if 'imgList' in data:
            self.img: list = data['imgList']

    def __repr__(self):
        return f'<NormSauce(title={repr(self.title)})>'


class GoogleNorm:
    def __init__(self, data):
        self.thumbnail = ""
        self.title = ""
        self.url = ""
        self._arrange(data)

    def _arrange(self, data):
        get_data = self._getdata(data)
        self.title = get_data['title']
        self.url = get_data['url']
        self.thumbnail = get_data['thumbnail']

    def _getdata(self, datas):

        data = {
            'thumbnail': "",
            'title': "",
            'url': "",
        }

        for x in datas:
            try:
                origin = x.find_all('h3')
                data['title'] = origin[0].string
                url = x.find_all('a')
                data['url'] = url[0]['href']
                img = self._gethumbnail(url)
                data['thumbnail'] = img
            except:
                pass

        return data

    @staticmethod
    def _gethumbnail(data):
        GOOGLEURL = "https://www.google.com/"
        regex = re.compile(
            r"((http(s)?(\:\/\/))+(www\.)?([\w\-\.\/])*(\.[a-zA-Z]{2,3}\/?))[^\s\b\n|]*[^.,;:\?\!\@\^\$ -]")

        thumbnail = "No directable url"

        for a in range(5):
            try:
                if re.findall('jpg|png', regex.search(data[a]['href']).group(1)):
                    thumbnail = regex.search(data[a]['href']).group(1)
                elif re.findall('/imgres', data[a]['href']):
                    thumbnail = f"{GOOGLEURL}{data[a]['href']}"
            except:
                continue

        return thumbnail

    def __repr__(self):
        return f'<NormGoogle(title={repr(self.title)}, url={self.url}, thumbnail={self.thumbnail})>'


class IqdbNorm:
    _URL = 'http://www.iqdb.org'

    def __init__(self, data):
        table = data.table
        self.content = ''
        self.url = ''
        self.title = ''
        self.thumbnail = ''
        self.size = ''
        self.similarity: float
        self._arrange(table)

    def _arrange(self, data):
        REGEXIQ = re.compile("[0-9]+")
        tbody = data.tr
        content = tbody.th.string
        self.content = content
        tbody = data.tr.next_sibling
        url = tbody.td.a['href'] if tbody.td.a['href'][:4] == "http" else "https:" + tbody.td.a['href']
        title = tbody.td.a.img['title']
        thumbnail = self._URL + tbody.td.a.img['src']
        tbody = tbody.next_sibling.next_sibling
        size = tbody.td.string
        tbody = tbody.next_sibling
        similarity_raw = REGEXIQ.search(tbody.td.string)
        similarity = float(similarity_raw.group(0))
        self.url = url
        self.title = title
        self.thumbnail = thumbnail
        self.size = size
        self.similarity = similarity

    def __repr__(self):
        return f'<NormIqdb(content={repr(self.content)}, similarity={repr(self.similarity)}'


class SauceNaoNorm:
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
        return f'<NormSauceNao(title={repr(self.title)}, similarity={self.similarity:.2f})>'


class TraceMoeNorm:
    def __init__(self, data, mute=False):
        self.origin: dict = data
        self.From: int = data['from']  # 匹配场景的开始时间
        self.To: int = data['to']  # 匹配场景的结束时间
        # 匹配的Anilist ID见https://anilist.co/
        self.anilist_id: int = data['anilist_id']
        self.at: int = data['at']  # 匹配场景的确切时间
        self.season: str = data['season']  # 发布时间
        self.anime: str = data['anime']  # 番剧名字
        self.filename: str = data['filename']  # 找到匹配项的文件名
        self.episode: int = data['episode']  # 估计的匹配的番剧的集数
        self.tokenthumb: str = data['tokenthumb']  # 用于生成预览的token
        self.similarity: float = float("{:.2f}".format(
            data['similarity'] * 100))  # 相似度，相似性低于 87% 的搜索结果可能是不正确的结果
        self.title: str = data['title']  # 番剧名字
        self.title_native: str = data['title_native']  # 番剧世界命名
        self.title_chinese: str = data['title_chinese']  # 番剧中文命名
        self.title_english: str = data['title_english']  # 番剧英文命名
        self.title_romaji: str = data['title_romaji']  # 番剧罗马命名
        # 匹配的MyAnimelist ID见https://myanimelist.net/
        self.mal_id: int = data['mal_id']
        self.synonyms: list = data['synonyms']  # 备用英文标题
        self.synonyms_chinese: list = data['synonyms_chinese']  # 备用中文标题
        self.is_adult: bool = data['is_adult']  # 是否R18
        self.thumbnail: str = self._preview_image()
        self.video_thumbnail: str = self._preview_video(mute)

    def _preview_image(self):  # 图片预览图
        # parse.quote()用于网页转码
        url = "https://trace.moe/thumbnail.php" \
              "?anilist_id={}&file={}&t={}&token={}".format(self.anilist_id, parse.quote(self.filename), self.at,
                                                            self.tokenthumb)
        return url

    def _preview_video(self, mute=False):
        """
        创建预览视频
        :param mute:预览视频是否静音，True为静音
        :return: 预览视频url地址
        """
        url = "https://media.trace.moe/video/" \
              f"{self.anilist_id}/{parse.quote(self.filename)}?t={self.at}&token={self.tokenthumb}"
        if mute:
            url = url + '&mute'
        return url

    @staticmethod
    def download_image(self, filename='image.png'):
        """
        下载缩略图
        :param filename: 重命名文件
        """
        with requests.get(self.thumbnail, stream=True) as resp:
            with open(filename, 'wb') as fd:
                for chunk in resp.iter_content():
                    fd.write(chunk)

    def download_video(self, filename='video.mp4'):
        """
        下载预览视频
        :param filename: 重命名文件
        """
        with requests.get(self.video_thumbnail, stream=True) as resp:
            with open(filename, 'wb') as fd:
                for chunk in resp.iter_content():
                    fd.write(chunk)

    def __repr__(self):
        return f'<NormTraceMoe(title={repr(self.title_native)}, similarity={self.similarity})>'