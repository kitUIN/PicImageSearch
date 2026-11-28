<div align="center">

# PicImageSearch

English | [简体中文](docs/zh/README.zh-CN.md) | [Русский](docs/ru/README.ru-RU.md) | [日本語](docs/ja/README.ja-JP.md)

✨ Aggregated Image Search Engine for Reverse Image Search ✨

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

<a href="https://pic-image-search.kituin.fun/">📖 Documentation</a>
·
<a href="https://github.com/kitUIN/PicImageSearch/issues/new">🐛 Submit an Issue</a>

</div>

## Supported Search Engines

| Engine              | Website                              | Notes                                        |
| ------------------- | ------------------------------------ | -------------------------------------------- |
| AnimeTrace          | <https://www.animetrace.com/>        | Also supports base64                         |
| ASCII2D             | <https://ascii2d.net/>               | May be blocked by Cloudflare, see `base_url` |
| Baidu               | <https://graph.baidu.com/>           |                                              |
| Bing                | <https://www.bing.com/images/search> | Requires a shared `client`                   |
| Copyseeker          | <https://copyseeker.net/>            | Requires a shared `client`                   |
| E-Hentai            | <https://e-hentai.org/>              | ExHentai requires cookies                    |
| Google (deprecated) | <https://www.google.com/imghp>       |                                              |
| Google Lens         | <https://lens.google.com/>           | Requires Google cookies                      |
| IQDB                | <https://iqdb.org/>                  |                                              |
| Lenso (deprecated)  | <https://lenso.ai/>                  |                                              |
| SauceNAO            | <https://saucenao.com/>              | Requires an API key                          |
| Tineye              | <https://tineye.com/search/>         | May be blocked by Cloudflare                 |
| TraceMoe            | <https://trace.moe/>                 | API key optional                             |
| Yandex              | <https://yandex.com/images/search>   |                                              |

## Usage

For detailed information, please refer to the [documentation](https://pic-image-search.kituin.fun/) or [example code](demo/code/).  
For `synchronous` usage, import using `from PicImageSearch.sync import ...` .  
For `asynchronous` usage, import using `from PicImageSearch import Network,...` .  
**Asynchronous usage is recommended.**

### Installation

- Requires Python 3.10 and above.
- Installation command: `pip install PicImageSearch`
- Or use the Tsinghua mirror: `pip install PicImageSearch -i https://pypi.tuna.tsinghua.edu.cn/simple`

## Star History

<a href="https://star-history.dera.page/#kitUIN/PicImageSearch">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://star-history.dera.page/svg?repos=kituin/picimagesearch&amp;theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://star-history.dera.page/svg?repos=kituin/picimagesearch" />
    <img alt="PicImageSearch star history chart" src="https://star-history.dera.page/svg?repos=kituin/picimagesearch" />
  </picture>
</a>
