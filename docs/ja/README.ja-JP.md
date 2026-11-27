<div align="center">

# PicImageSearch

[English](../../README.md) | [简体中文](../zh/README.zh-CN.md) | [Русский](../ru/README.ru-RU.md) | 日本語

✨ 画像検索アグリゲーター ✨

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

<a href="https://pic-image-search.kituin.fun/">📖 ドキュメント</a>
·
<a href="https://github.com/kitUIN/PicImageSearch/issues/new">🐛 問題を報告</a>

</div>

## サポート

| エンジン            | ウェブサイト                         | 備考                                                   |
| ------------------- | ------------------------------------ | ------------------------------------------------------ |
| AnimeTrace          | <https://www.animetrace.com/>        | base64 にも対応                                        |
| ASCII2D             | <https://ascii2d.net/>               | Cloudflare にブロックされる場合あり、`base_url` を参照 |
| Baidu               | <https://graph.baidu.com/>           |                                                        |
| Bing                | <https://www.bing.com/images/search> | 共有の `client` が必要                                 |
| Copyseeker          | <https://copyseeker.net/>            | 共有の `client` が必要                                 |
| E-Hentai            | <https://e-hentai.org/>              | ExHentai は cookies が必要                             |
| Google (deprecated) | <https://www.google.com/imghp>       |                                                        |
| Google Lens         | <https://lens.google.com/>           | Google の cookies が必要                               |
| IQDB                | <https://iqdb.org/>                  |                                                        |
| Lenso (deprecated)  | <https://lenso.ai/>                  |                                                        |
| SauceNAO            | <https://saucenao.com/>              | API キーが必要                                         |
| Tineye              | <https://tineye.com/search/>         | Cloudflare にブロックされる場合あり                    |
| TraceMoe            | <https://trace.moe/>                 | API キーは任意                                         |
| Yandex              | <https://yandex.com/images/search>   |                                                        |

## 使用方法

詳細は [ドキュメント](https://pic-image-search.kituin.fun/) または [デモコード](demo/code/) を参照してください。  
`同期`を使用する場合は `from PicImageSearch.sync import ...` をインポートしてください。  
`非同期`を使用する場合は `from PicImageSearch import Network,...` をインポートしてください。  
**非同期の使用を推奨します。**

### インストール

- Python 3.10 以降が必要です。
- インストール: `pip install PicImageSearch`
- または Tsinghua ミラーを使用: `pip install PicImageSearch -i https://pypi.tuna.tsinghua.edu.cn/simple`

## スター履歴

<a href="https://star-history.dera.page/#kitUIN/PicImageSearch">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://star-history.dera.page/svg?repos=kituin/picimagesearch&amp;theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://star-history.dera.page/svg?repos=kituin/picimagesearch" />
    <img alt="PicImageSearch のスター履歴グラフ" src="https://star-history.dera.page/svg?repos=kituin/picimagesearch" />
  </picture>
</a>
