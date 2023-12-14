---
title: 🔖 Changelog
date: 2021-03-27
permalink: /wiki/picimagesearch/releases
article: false
---

## [3.9.2](https://github.com/kitUIN/PicImageSearch/releases/tag/v3.9.2)

fix(baidu): `similarity` and `title` fields are deprecated because Baidu no longer provides `simi` and `fromPageTitle`
fields

## [3.9.1](https://github.com/kitUIN/PicImageSearch/releases/tag/v3.9.1)

fix(google): correct thumbnail parser logic
build(deps): update dependencies

## [3.9.0](https://github.com/kitUIN/PicImageSearch/releases/tag/v3.9.0)

fix(google): remove the `goto_page()` method, add `pre_page()` and `next_page()` methods, make changes to the attributes
of `GoogleResponse`

BREAKING CHANGE: the `goto_page()`` method is no longer available and some attributes of `GoogleResponse` have been
modified

refactor(bypass): remove DoH related logic
refactor: replace `aiohttp` with `httpx`
refactor: remove redundant `_slice()` methods and standardize the structure of each module
feat(yandex): add a new reverse image search engine `Yandex`
chore: add `.pre-commit-config.yaml` file
style(network): remove unused logic

## [3.8.0](https://github.com/kitUIN/PicImageSearch/releases/tag/v3.8.0)

feat(Google): extract base64 from Google thumbnail
fix(Google): fix extract base64 logic from Google thumbnail
fix(google): correct page redirection logic and refactor code
build(deps): update dependencies
chore(ruff): add ruff configuration
style: split long lines into multiple shorter lines

## [3.7.8](https://github.com/kitUIN/PicImageSearch/releases/tag/v3.7.8)

🐛 修正 `ehentai` 搜索结果的解析逻辑

## [3.7.7](https://github.com/kitUIN/PicImageSearch/releases/tag/v3.7.7)

🐛 修正 `ehentai` 搜索结果的解析逻辑

## [3.7.6](https://github.com/kitUIN/PicImageSearch/releases/tag/v3.7.6)

🐛 修正 `ehentai` 缩略图地址的获取逻辑

## [3.7.5](https://github.com/kitUIN/PicImageSearch/releases/tag/v3.7.5)

⬆️ 依赖升级

## [3.7.4](https://github.com/kitUIN/PicImageSearch/releases/tag/v3.7.4)

🐛 `ehentai` 搜索结果被用户设置的过滤器过滤掉时，当作搜索结果为空

## [3.7.3](https://github.com/kitUIN/PicImageSearch/releases/tag/v3.7.3)

🐛 修正 `ascii2d` 搜索结果的解析逻辑

## [3.7.2](https://github.com/kitUIN/PicImageSearch/releases/tag/v3.7.2)

🐛 修正 `ascii2d` 搜索结果的解析逻辑

## [3.7.1](https://github.com/kitUIN/PicImageSearch/releases/tag/v3.7.1)

✨ `iqdb` `saucenao` 返回对象增加 `url`

♻️ `ascii2d` 增加对来源为 `seiga` 或 `nijie` 的处理

🐛 修正 `ascii2d` 搜索结果的解析逻辑

## [3.7.0](https://github.com/kitUIN/PicImageSearch/releases/tag/v3.7.0)

♻️ `saucenao` 返回结果增加 `ext_urls` `author_url` `source` ，去除 `pixiv_id` 和 `member_id`

✨ 为 `Network` 添加参数 `verify_ssl`

⬆️ 依赖升级

## [3.6.1](https://github.com/kitUIN/PicImageSearch/releases/tag/v3.6.1)

🐛 修正 `ascii2d` 搜索结果的解析逻辑

## [3.6.0](https://github.com/kitUIN/PicImageSearch/releases/tag/v3.6.0)

♻️ 重构 `ascii2d` 搜索结果的获取和解析逻辑，及返回的结果

## [3.5.1](https://github.com/kitUIN/PicImageSearch/releases/tag/v3.5.1)

♻️ 重构 `baidu` 返回的结果

## [3.5.0](https://github.com/kitUIN/PicImageSearch/releases/tag/v3.5.0)

♻️ 重构 `baidu` 搜索结果的获取和解析逻辑，及返回的结果样式

## [3.4.4](https://github.com/kitUIN/PicImageSearch/releases/tag/v3.4.4)

🐛 修正 `ehentai` 搜索结果的预览图解析逻辑

## [3.4.3](https://github.com/kitUIN/PicImageSearch/releases/tag/v3.4.3)

🐛 修正 `ascii2d` 搜索结果的解析逻辑

## [3.4.2](https://github.com/kitUIN/PicImageSearch/releases/tag/v3.4.2)

🐛 修正 `ehentai` 搜索结果的解析逻辑

## [3.4.1](https://github.com/kitUIN/PicImageSearch/releases/tag/v3.4.1)

✨ search 参数 `file` 增加 `bytes` 类型支持

## [3.4.0](https://github.com/kitUIN/PicImageSearch/releases/tag/v3.4.0)

♻️ 重构 search 参数 `file` 为 `str` / `Path` 类型

💥 BREAKING CHANGE: 如果有用到上传文件搜索，请跟进这个改动

## [3.3.11](https://github.com/kitUIN/PicImageSearch/releases/tag/3.3.11)

🐛 `saucenao` 当 `_get_title` 在遇到获取到 `None` 时返回空字符串

## [3.3.10](https://github.com/kitUIN/PicImageSearch/releases/tag/3.3.10)

✨ 添加 `timeout` 为可配置参数

## [3.3.9](https://github.com/kitUIN/PicImageSearch/releases/tag/3.3.9)

🐛 修正 `iqdb` `_arrange` 的逻辑

## [3.3.8](https://github.com/kitUIN/PicImageSearch/releases/tag/3.3.8)

⬆️ 用 `aiohttp` 替代 `httpx` ，提高性能和扩展性 by @[NekoAria](https://github.com/NekoAria)

> ⛏️Merged From [#26](https://github.com/kitUIN/PicImageSearch/pull/26) by [@chinoll](https://github.com/chinoll)

✨ 添加绕过 `DNS` 污染的参数 by @[chinoll](https://github.com/chinoll) & @[NekoAria](https://github.com/NekoAria)

✨ 支持 `sock5 / socks4` 代理 (可选功能)  by @[NekoAria](https://github.com/NekoAria)

✖️ 依赖更新，同时不再支持 `python 3.6`

## [3.3.7](https://github.com/kitUIN/PicImageSearch/releases/tag/3.3.7)

✨ `tracemoe` 增加 5 个字段：`type` `format` `start_date` `end_date` `cover_image`

♻️ 重构获取动画信息的相关逻辑 by [#24](https://github.com/kitUIN/PicImageSearch/issues/24)

## [3.3.6](https://github.com/kitUIN/PicImageSearch/releases/tag/3.3.6)

✨ `saucenao` 搜索结果增加一个字段 `hidden` (是否为搜索引擎参数 `hide` 对应的 `NSFW` 内容)

## [3.3.5](https://github.com/kitUIN/PicImageSearch/releases/tag/3.3.5)

✨ `ascii2d` 搜索结果增加一个字段 `url`

## [3.3.4](https://github.com/kitUIN/PicImageSearch/releases/tag/3.3.4)

♻️ 针对上传图片进行搜索时因为图片过大或上行速度过慢导致的 `httpx.ReadTimeout` ，延长 `read` 时的超时时长

## [3.3.3](https://github.com/kitUIN/PicImageSearch/releases/tag/3.3.3)

✨ `ascii2d` 搜索结果增加一个字段 `hash`
⬆️ Bump actions/setup-python from 3 to 4

## [3.3.2](https://github.com/kitUIN/PicImageSearch/releases/tag/3.3.2)

> ⛏️Merged From [#23](https://github.com/kitUIN/PicImageSearch/pull/23) by [@chinoll](https://github.com/chinoll)

🐛 修正 `ascii2d` 在某些情况下遇到 `title` 为空的情况

## [3.3.1](https://github.com/kitUIN/PicImageSearch/releases/tag/3.3.1)

🐛 修正 `saucenao` 搜索遇到 `HTTP` 状态码为 `429` 时的处理逻辑

## [3.3.0](https://github.com/kitUIN/PicImageSearch/releases/tag/3.3.0)

♻️ 将 `search()` 的参数为 `URL` 或本地文件区分开

## [3.2.0](https://github.com/kitUIN/PicImageSearch/releases/tag/3.2.0)

✨ `Saucenao` 增加新参数 `dbs` ，用来设置多个数据库索引
🎨 改进结构和代码格式

## [3.1.9](https://github.com/kitUIN/PicImageSearch/releases/tag/3.1.9)

♻️ 去除不必要的 `async/await`
🐛 修正 `TraceMoeItem` 中对 `similarity` 的处理逻辑

## [3.1.8](https://github.com/kitUIN/PicImageSearch/releases/tag/3.1.8)

♻️ 调整请求超时的设置回最初的版本

## [3.1.7](https://github.com/kitUIN/PicImageSearch/releases/tag/3.1.7)

🐛 修复部分情况下 `EHentai` 拿到的缩略图不对的问题

## [3.1.6](https://github.com/kitUIN/PicImageSearch/releases/tag/3.1.6)

✨ `EHentai` 搜图支持网络地址而不仅是本地文件

## [3.1.5](https://github.com/kitUIN/PicImageSearch/releases/tag/3.1.5)

🐛 修正 `tracemoe` 的部分逻辑

## [3.1.4](https://github.com/kitUIN/PicImageSearch/releases/tag/3.1.4)

🐛 修正 `tracemoe` 的部分逻辑

## [3.1.3](https://github.com/kitUIN/PicImageSearch/releases/tag/3.1.3)

♻️ 重构 `tracemoe` 获取中文标题相关逻辑，并多提供一个 `anime_info` 属性

## [3.1.2](https://github.com/kitUIN/PicImageSearch/releases/tag/3.1.2)

♻️ 重构代码

- 合并 `iqdb3d` 的搜索逻辑到 `iqdb` ，由参数 `is_3d` 决定，另添加新搜索参数 `force_gray` (忽略颜色)
- 会话延长超时参数，并加入重试
  🔥 移除日志打印相关逻辑，只保留 `demo` 中的

## [3.1.1](https://github.com/kitUIN/PicImageSearch/releases/tag/3.1.1)

🐛 修复 `EXHentai` 搜索拿不到 `cookies 的问题 `

- python 最低版本为 `3.6`

## [3.1.0](https://github.com/kitUIN/PicImageSearch/releases/tag/3.1.0)

✨ 新增 `EHentai` 搜图
🎨 改进结构和代码格式

## [3.0.1](https://github.com/kitUIN/PicImageSearch/releases/tag/3.0.1)

♻️ 重构代码

- 用 `event_hooks` 处理请求出错的情况
- 用 `pyquery` 替换 `beautifulsoup`
- 优化返回对象的结构和逻辑
- 重写测试用例

## [2.3.1](https://github.com/kitUIN/PicImageSearch/releases/tag/2.3.1)

♻️大量重构，合并重复逻辑，提供 `sync.syncify` 魔改异步逻辑为同步

- `python` 最低版本为 `3.6`

## [2.3.0](https://github.com/kitUIN/PicImageSearch/releases/tag/2.3.0)

🐛 Fix [#7](https://github.com/kitUIN/PicImageSearch/issues/7) ： 修复百度识图功能

👷 更换打包方式

## [2.2.9](https://github.com/kitUIN/PicImageSearch/releases/tag/2.2.9)

> ⛏️Merged From [#19](https://github.com/kitUIN/PicImageSearch/pull/19)

♻️ 重构代码

- 去除 `cloudscraper` 、 `requests` 和 `MultipartEncoder` ，改为使用 `httpx`

## [2.2.8](https://github.com/kitUIN/PicImageSearch/releases/tag/2.2.8)

> ⛏️Merged From [#16](https://github.com/kitUIN/PicImageSearch/pull/16)

🎨 改进结构和代码格式

## [2.2.7](https://github.com/kitUIN/PicImageSearch/releases/tag/2.2.7)

> ⛏️Merged From [#15](https://github.com/kitUIN/PicImageSearch/pull/15)

✨ 添加新特性： 为异步的 ascii2d 加上特征检索

♻️ 重构代码

- 将每个类中重复的 `_errors()` 静态方法独立出来
- 去除没用到的模块

## New Collaborator

::: cardList

```yaml
- name: Neko Aria
  desc: _(:3」∠)_
  avatar: http://q1.qlogo.cn/g?b=qq&nk=990879119&s=640
  link: https://github.com/NekoAria
  bgColor: '#CBEAFA'
  textColor: '#6854A1'
```

:::
> Mar 14, 2022

## [2.2.5](https://github.com/kitUIN/PicImageSearch/releases/tag/2.2.5)

提供数据类型显示
![QQ 截图 20220118165255](https://user-images.githubusercontent.com/68675068/149904102-a7ba2181-d7c0-4486-8607-1b485f7a1431.png)
![QQ 截图 20220118165203](https://user-images.githubusercontent.com/68675068/149904105-8a2303af-fca4-4706-85fe-d9d81edb6bd8.png)

## [2.2.3](https://github.com/kitUIN/PicImageSearch/releases/tag/2.2.3)

🐛fix `ascii2d` bug [#13](https://github.com/kitUIN/PicImageSearch/issues/13)

## [2.2.2](https://github.com/kitUIN/PicImageSearch/releases/tag/2.2.2)

✨`Iqdb` 异步实现

## [2.2.1](https://github.com/kitUIN/PicImageSearch/releases/tag/2.2.1)

> ⛏️Merged From [#12](https://github.com/kitUIN/PicImageSearch/pull/12)

🐛 修复 `iqdb bug` [#11](https://github.com/kitUIN/PicImageSearch/issues/11)
🎨 更改部分 `iqdb` 结构
🎨 `Ascii2d` 特征搜索

## [2.1.2](https://github.com/kitUIN/PicImageSearch/releases/tag/2.1.2)

✨支持翻页 [#10](https://github.com/kitUIN/PicImageSearch/issues/10)

## [2.1.1](https://github.com/kitUIN/PicImageSearch/releases/tag/2.1.1)

🐛fix bug [#9](https://github.com/kitUIN/PicImageSearch/issues/9)

## [2.1.0](https://github.com/kitUIN/PicImageSearch/releases/tag/2.1.0)

✨添加异步用法

## [2.0.5](https://github.com/kitUIN/PicImageSearch/releases/tag/2.0.5)

🎨修正数据结构

## [2.0.4](https://github.com/kitUIN/PicImageSearch/releases/tag/2.0.4)

🎨修正数据结构

## [2.0.3](https://github.com/kitUIN/PicImageSearch/releases/tag/2.0.3)

🐛`TraceMoe` 番剧中文名称获取

## [2.0.2](https://github.com/kitUIN/PicImageSearch/releases/tag/2.0.2)

⬆️更新 `TraceMoe API`

- 添加自我信息查询

## [2.0.1](https://github.com/kitUIN/PicImageSearch/releases/tag/2.0.1)

⬆️更新了 TraceMoe API

## [1.2.0](https://github.com/kitUIN/PicImageSearch/releases/tag/1.2.0)

🐛fix google title, some python couldn't install package [#4](https://github.com/kitUIN/PicImageSearch/pull/4)

## [1.0.1](https://github.com/kitUIN/PicImageSearch/releases/tag/1.0.1)

- 添加百度识图支持
- 文档独立为网站，不再使用 `wiki`
- 调整支持库
- `TraceMoe` 的请求 `url` 调整 [#3](https://github.com/kitUIN/PicImageSearch/pull/3)

## [0.8.2](https://github.com/kitUIN/PicImageSearch/releases/tag/0.8.2)

- 支持 `Iqdb 3d`
- 支持 `google`

## [0.6.7](https://github.com/kitUIN/PicImageSearch/releases/tag/0.6.7)

- 代理模式常驻
- 修订 `wiki`
- 更新上传文件方式
- 支持 `Ascii2d API`
- 支持库调整

## [0.6.4](https://github.com/kitUIN/PicImageSearch/releases/tag/0.6.4)

- `TraceMoe` 代码格式化
- `SauceNAO` 访问增加代理
- 修订 `wiki`
- `'Connection aborted.', ConnectionResetError(104, 'Connection reset by peer')`
    - 一个解决方法：使用代理

## [0.6.3](https://github.com/kitUIN/PicImageSearch/releases/tag/0.6.3)

- 完善了所有类型 `params`
- 修订 `wiki`

## [0.6.0](https://github.com/kitUIN/PicImageSearch/releases/tag/0.6.0)

- 添加 `SauceNAO` 搜图引擎
- 添加 `TraceMoe` 注释
- 建立 `wiki`  

