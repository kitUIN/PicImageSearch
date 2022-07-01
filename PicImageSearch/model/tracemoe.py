from typing import Any, Dict, List, Optional


class TraceMoeMe:
    def __init__(self, data: Dict[str, Any]):
        self.id: str = data["id"]  # IP 地址（访客）或电子邮件地址（用户）
        self.priority: int = data["priority"]  # 优先级
        self.concurrency: int = data["concurrency"]  # 搜索请求数量
        self.quota: int = data["quota"]  # 本月的搜索配额
        self.quotaUsed: int = data["quotaUsed"]  # 本月已经使用的搜索配额


class TraceMoeItem:
    def __init__(
        self,
        data: Dict[str, Any],
        mute: bool = False,
        size: Optional[str] = None,
    ):
        """

        :param data: 数据
        :param mute: 预览视频静音
        :param size: 视频与图片大小(s/m/l)
        """
        self.origin: Dict[str, Any] = data  # 原始数据
        self.anime_info: Dict[str, Any] = {}  # 动画信息
        self.idMal: int = 0  # 匹配的MyAnimelist ID见https://myanimelist.net/
        self.title: Dict[str, str] = {}
        self.title_native: str = ""
        """番剧国际命名"""
        self.title_english: str = ""
        self.title_romaji: str = ""
        self.title_chinese: str = ""
        self.anilist: int = data["anilist"]  # 匹配的Anilist ID见https://anilist.co/
        self.synonyms: List[str] = []  # 备用英文标题
        self.isAdult: bool = False
        self.type: str = ""
        self.format: str = ""
        self.start_date: Dict[str, Any] = {}
        self.end_date: Dict[str, Any] = {}
        self.cover_image: str = ""
        self.filename: str = data["filename"]
        self.episode: int = data["episode"]
        self.From: float = data["from"]
        self.To: float = data["to"]
        self.similarity: float = float(f"{data['similarity'] * 100:.2f}")
        self.video: str = data["video"]
        self.image: str = data["image"]
        if size in ["l", "s", "m"]:  # 大小设置
            self.video += f"&size={size}"
            self.image += f"&size={size}"
        if mute:  # 视频静音设置
            self.video += "&mute"


class TraceMoeResponse:
    def __init__(
        self,
        data: Dict[str, Any],
        mute: bool,
        size: Optional[str],
    ):
        self.origin: Dict[str, Any] = data  # 原始数据
        self.raw: List[TraceMoeItem] = []  # 结果返回值
        res_docs = data["result"]
        self.raw.extend(
            [
                TraceMoeItem(
                    i,
                    mute=mute,
                    size=size,
                )
                for i in res_docs
            ]
        )
        self.frameCount: int = data["frameCount"]  # 搜索的帧总数
        self.error: str = data["error"]  # 错误报告
