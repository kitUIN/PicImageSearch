#! /usr/bin/env python3
# coding=utf-8
import requests, base64
from urllib import parse
class TraceMoe:
    def __init__(self):
        self.Url = 'https://trace.moe/api/search'#按图像 URL 搜索
        self.img = ''#本地图片base64转码结果
        self.raws = []
    def base_64(self, filename):
        with open(filename, 'rb') as f:
            coding = base64.b64encode(f.read())  # 读取文件内容，转换为base64编码
            print('本地base64转码~')
            return coding.decode()
    def errors(self,code):
        if code == 200:
            response = 'trace.moe访问正常。'
            return response
        elif code == 413:
            response = '图片体积太大。'
            return response
        elif code == 400:
            response = '你没上传图片？'
            return response
        elif code == 403:
            response = 'token无效。'
            return response
        elif code == 429:
            response = '请求太快了，缓一缓吧。'
            return response
        elif code == 500 or code == 503:
            response = '服务器错误 或者 你传错了图片格式。'
            return response            
        else:
            response = '未知错误'
            return response
    def arrange(self, data):                                    #整理数据
        self.raw_all = data                                     #总返回
        self.RawDocsCount = data['RawDocsCount']                #搜索的帧总数
        self.RawDocsSearchTime = data['RawDocsSearchTime']      #从数据库检索帧所用的时间
        self.ReRankSearchTime = data['ReRankSearchTime']        #比较帧所用的时间
        self.CacheHit = data['CacheHit']                        #是否缓存搜索结果
        self.trial = data['trial']                              #搜索时间
        self.limit = data['limit']                              #剩余搜索限制数
        self.limit_ttl = data['limit_ttl']                      #限制重置之前的时间（秒）
        self.quota = data['quota']                              #剩余搜索配额数
        self.quota_ttl = data['quota_ttl']                      #配额重置之前的时间（秒）
        docs = data['docs'][0]
        self.raw = docs                                         #最匹配项总结果
        self.From = docs['from']                                #匹配场景的开始时间
        self.to = docs['to']                                    #匹配场景的结束时间
        self.anilist_id = docs['anilist_id']                    #匹配的Anilist  IDhttps://anilist.co/
        self.at = docs['at']                                    #匹配场景的确切时间
        self.season = docs['season']                            #发布时间
        self.anime = docs['anime']                              #番剧名字
        self.filename = docs['filename']                        #找到匹配项的文件名
        self.episode = docs['episode']                          #估计的匹配的番剧的集数
        self.tokenthumb = docs['tokenthumb']                    #用于生成预览的token
        self.similarity = docs['similarity']                    #相似度，相似性低于 87% 的搜索结果可能是不正确的结果
        self.title = docs['title']                              #番剧名字
        self.title_native = docs['title_native']                #番剧世界命名
        self.title_chinese = docs['title_chinese']              #番剧中文命名
        self.title_english = docs['title_english']              #番剧英文命名
        self.title_romaji = docs['title_romaji']                #番剧罗马命名
        self.mal_id = docs['mal_id']                            #匹配的MyAnimelist  IDhttps://myanimelist.net/
        self.synonyms = docs['synonyms']                        #备用英文标题
        self.synonyms_chinese = docs['synonyms_chinese']        #备用中文标题
        self.is_adult = docs['is_adult']                        #是否R18
        self.thumbnail = self.preview_image()                   #缩略图预览地址
        self.viedo = self.preview_video()                       #视频预览地址
        for i in range(len(data['docs'])):
            self.raws.append(data['docs'][i])                   #分开搜索结果
    def preview_image(self):#预览
        anilist_id = self.anilist_id
        filename = parse.quote(self.filename)
        at = self.at
        tokenthumb = self.tokenthumb
        url = "https://trace.moe/thumbnail.php?anilist_id={}&file={}&t={}&token={}".format(anilist_id,filename,at,tokenthumb)
        return url

    def preview_video(self, mute=True):
        anilist_id = self.anilist_id
        filename = parse.quote(self.filename)
        at = self.at
        tokenthumb = self.tokenthumb
        url = 'https://media.trace.moe/video/{}/{}?t={}&token={}'.format(anilist_id,filename,at,tokenthumb)
        if mute:
            url = url + '&mute'
        return url
    def search(self, url, file=False, Filter=0):
        try: 
            if file : #是否是本地文件
                URl = self.Url 
                self.img = self.base_64(url)
                res = requests.post(URl, json={"image": self.img,"filter": 0})   
            elif not file:#网络url
                URl = self.Url +'?url=' + url
                res = requests.get(URl)
            error = self.errors(res.status_code)
            print(error)
            data = res.json()
            self.arrange(data)
        except Exception as e:
            print(e)
    def download_image(self,thumbnail):
        with requests.get(thumbnail, stream=True) as resp:
            with open('image.png', 'wb') as fd:
                for chunk in resp.iter_content():
                    fd.write(chunk)
    def download_video(self,video):
        with requests.get(video, stream=True) as resp:
            with open('video.mp4', 'wb') as fd:
                for chunk in resp.iter_content():
                    fd.write(chunk)
