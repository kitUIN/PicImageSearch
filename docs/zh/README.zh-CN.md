<div align="center">

# PicImageSearch

[English](../../README.md) | 简体中文 | [Русский](../ru/README.ru-RU.md) | [日本語](../ja/README.ja-JP.md)

✨ 聚合识图引擎 用于以图搜源 ✨

<a href="https://raw.githubusercontent.com/kitUIN/PicImageSearch/master/LICENSE">
    <img src="https://img.shields.io/github/license/kitUIN/PicImageSearch" alt="license">
</a>
<a href="https://pypi.python.org/pypi/PicImageSearch">
    <img src="https://img.shields.io/pypi/v/PicImageSearch" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.10+-blue" alt="python">
<a href="https://github.com/kitUIN/PicImageSearch/releases">
    <img src="https://img.shields.io/github/v/release/kitUIN/PicImageSearch" alt="release">
</a>
<a href="https://github.com/kitUIN/PicImageSearch/issues">
    <img src="https://img.shields.io/github/issues/kitUIN/PicImageSearch" alt="issues">
</a>

<a href="https://pic-image-search.kituin.fun/">📖 文档</a>
·
<a href="https://github.com/kitUIN/PicImageSearch/issues/new">🐛 提交问题</a>

</div>

## 支持的搜索引擎

| 引擎                | 网站                                 | 备注                                      |
| ------------------- | ------------------------------------ | ----------------------------------------- |
| AnimeTrace          | <https://www.animetrace.com/>        | 也支持 base64                             |
| ASCII2D             | <https://ascii2d.net/>               | 可能被 Cloudflare 拦截，可使用 `base_url` |
| Baidu               | <https://graph.baidu.com/>           |                                           |
| Bing                | <https://www.bing.com/images/search> | 需要共享的 `client`                       |
| Copyseeker          | <https://copyseeker.net/>            | 需要共享的 `client`                       |
| E-Hentai            | <https://e-hentai.org/>              | ExHentai 需要 cookies                     |
| Google (deprecated) | <https://www.google.com/imghp>       |                                           |
| Google Lens         | <https://lens.google.com/>           | 需要 Google cookies                       |
| IQDB                | <https://iqdb.org/>                  |                                           |
| Lenso (deprecated)  | <https://lenso.ai/>                  |                                           |
| SauceNAO            | <https://saucenao.com/>              | 需要 API key                              |
| Tineye              | <https://tineye.com/search/>         | 可能被 Cloudflare 拦截                    |
| TraceMoe            | <https://trace.moe/>                 | API key 可选                              |
| Yandex              | <https://yandex.com/images/search>   |                                           |

## 使用方法

详细信息请参阅 [文档](https://pic-image-search.kituin.fun/) 或者 [示例代码](demo/code/)。  
`同步`请使用 `from PicImageSearch.sync import ...` 导入。  
`异步`请使用 `from PicImageSearch import Network,...` 导入。  
**推荐使用异步。**

### 安装

- 需要 Python 3.10 及以上版本。
- 安装命令：`pip install PicImageSearch`
- 或使用清华镜像：`pip install PicImageSearch -i https://pypi.tuna.tsinghua.edu.cn/simple`

## 星标历史

<a href="https://star-history.dera.page/#kitUIN/PicImageSearch">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://star-history.dera.page/svg?repos=kituin/picimagesearch&amp;theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://star-history.dera.page/svg?repos=kituin/picimagesearch" />
    <img alt="PicImageSearch 星标历史图" src="https://star-history.dera.page/svg?repos=kituin/picimagesearch" />
  </picture>
</a>
