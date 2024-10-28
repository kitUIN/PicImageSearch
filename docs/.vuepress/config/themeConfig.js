const htmlModules = require("./htmlModules");
const nav = require("./nav.js");
const jpNav = require("./jp/nav.js");
const ruNav = require("./ru/nav.js");
const zhNav = require("./zh/nav.js");

module.exports = {
    sidebarDepth: 2, // 侧边栏显示深度，默认 1，最大 2（显示到 h3 标题）
    logo: 'https://avatars.githubusercontent.com/u/68675068?v=4', // 导航栏 logo
    repo: 'kitUIN/PicImageSearch', // 导航栏右侧生成 Github 链接
    searchMaxSuggestions: 10, // 搜索结果显示最大数
    lastUpdated: '上次更新', // 更新的时间，及前缀文字   string | boolean (取值为 git 提交时间)

    docsDir: 'docs', // 编辑的文件夹
    docsBranch: 'docs',
    editLinks: true, // 编辑链接
    editLinkText: '编辑',

    // 以下配置是 Vdoing 主题改动的和新增的配置
    sidebar: {mode: 'structuring', collapsable: true}, // 侧边栏  'structuring' | { mode: 'structuring', collapsable: Boolean} | 'auto' | 自定义    温馨提示：目录页数据依赖于结构化的侧边栏数据，如果你不设置为'structuring', 将无法使用目录页

    // sidebarOpen: false, // 初始状态是否打开侧边栏，默认 true
    updateBar: { // 最近更新栏
        showToArticle: false, // 显示到文章页底部，默认 true
        // moreArticle: '/archives' // “更多文章”跳转的页面，默认'/archives'
    },
    // titleBadge: false, // 文章标题前的图标是否显示，默认 true
    // titleBadgeIcons: [ // 文章标题前图标的地址，默认主题内置图标
    //   '图标地址1',
    //   '图标地址2'
    // ],

    pageStyle: 'line', // 页面风格，可选值：'card'卡片 | 'line' 线（未设置 bodyBgImg 时才生效）， 默认'card'。 说明：card 时背景显示灰色衬托出卡片样式，line 时背景显示纯色，并且部分模块带线条边框

    // contentBgStyle: 1,

    category: false, // 是否打开分类功能，默认 true。 如打开，会做的事情有：1. 自动生成的 frontmatter 包含分类字段 2. 页面中显示与分类相关的信息和模块 3. 自动生成分类页面（在 @pages 文件夹）。如关闭，则反之。
    tag: false, // 是否打开标签功能，默认 true。 如打开，会做的事情有：1. 自动生成的 frontmatter 包含标签字段 2. 页面中显示与标签相关的信息和模块 3. 自动生成标签页面（在 @pages 文件夹）。如关闭，则反之。
    // archive: false, // 是否打开归档功能，默认 true。 如打开，会做的事情有：1. 自动生成归档页面（在 @pages 文件夹）。如关闭，则反之。

    author: {// 文章默认的作者信息，可在 md 文件中单独配置此信息 String | {name: String, href: String}
        name: 'kitUIN', // 必需
        href: 'https://github.com/kitUIN' // 可选的
    },
    social: { // 社交图标，显示于博主信息栏和页脚栏
        // iconfontCssFile: '//at.alicdn.com/t/font_1678482_u4nrnp8xp6g.css', // 可选，阿里图标库在线 css 文件地址，对于主题没有的图标可自由添加
        icons: [{
            iconClass: 'icon-youjian',
            title: '发邮件',
            link: 'mailto:kulujun@gmail.com',
        },
            {
                iconClass: 'icon-bilibili',
                title: 'BILIBILI',
                link: 'https://space.bilibili.com/61924180',
            },
            {
                iconClass: 'icon-github',
                title: 'GitHub',
                link: 'https://github.com/kitUIN',
            },
        ],
    },
    footer: {
        // 页脚信息
        createYear: 2021, // 博客创建年份
        copyrightInfo: 'kitUIN | <a href="https://github.com/xugaoyi/vuepress-theme-vdoing/blob/master/LICENSE" target="_blank">MIT License</a>', // 博客版权信息，支持 a 标签
    },
    htmlModules,
    locales: {
        '/': {
            nav: nav,
            selectText: '🌐 Languages',
            label: 'English',
            editLinkText: 'Edit this page on GitHub',
        },
        '/zh/': {
            nav: zhNav,
            selectText: '🌐 选择语言',
            label: '简体中文',
            editLinkText: '在 GitHub 上编辑此页',
        },
        '/ru/': {
            nav: ruNav,
            selectText: '🌐 Выберите язык',
            label: 'Русский',
            editLinkText: 'Редактировать эту страницу на GitHub',
        },
        '/jp/': {
            nav: jpNav,
            selectText: '🌐 言語を選択',
            label: '日本語',
            editLinkText: 'このページを GitHub で編集',
        }
    }
}
