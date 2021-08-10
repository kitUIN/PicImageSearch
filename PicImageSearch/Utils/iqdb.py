import re

from bs4 import BeautifulSoup


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
        return f'<NormIqdb(content={repr(self.content)}, title={repr(self.title)}, similarity={repr(self.similarity)}>'


class IqdbResponse:
    def __init__(self, resp):
        self.origin: list = resp
        self.raw: list = list()
        self._slice(resp)

    def _slice(self, data):
        soup = BeautifulSoup(data, "html.parser", from_encoding='utf-8')
        pages = soup.find(attrs={"class": "pages"})
        for i in pages:
            if i == '\n' or str(i) == '<br/>' or 'Your image' in str(i):
                continue
            self.raw.append(IqdbNorm(i))

    def __repr__(self):
        return f'<IqdbResponse(count={repr(len(self.raw))})>'
