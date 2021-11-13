import re


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


class GoogleResponse:

    def __init__(self, resp, pages, index):
        self.origin: list = resp
        self.raw: list = list()
        self.index: int = index
        self.page: int = len(pages)
        self.pages: list = pages

        for ele in self.origin:
            detail = ele.contents
            self.raw.append(GoogleNorm(detail))

    def get_page_url(self, index):
        if self.index != index:
            url = "https://www.google.com" + self.pages[index - 1].a['href']
            print(url)
            return url

    def __repr__(self):
        return f'<GoogleResponse(count{repr(len(self.origin))})>'
