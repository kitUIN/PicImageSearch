const head = require('./config/head.js');
const plugins = require('./config/plugins.js'); // 插件
const themeConfig = require('./config/themeConfig.js'); // 主题配置


module.exports = {

    theme: 'vdoing', // 使用依赖包主题
    // theme: require.resolve('../../vdoing'), // 使用本地主题 ( 先将 vdoing 主题文件下载到本地：https://github.com/xugaoyi/vuepress-theme-vdoing)
    title: "PicImageSearch",
    description: '✨ 聚合识图引擎 用于以图搜源✨',
    // base: '/', // 默认'/'。如果你想将你的网站部署到如 https://foo.github.io/bar/，那么 base 应该被设置成 "/bar/",（否则页面将失去样式等文件）
    head, // 注入到页面 <head> 中的标签，格式 [tagName, { attrName: attrValue}, innerHTML?]
    themeConfig,
    plugins,

    markdown: {
        // lineNumbers: true,
        extractHeaders: ['h2', 'h3', 'h4', 'h5', 'h6'], // 提取标题到侧边栏的级别，默认 ['h2', 'h3']
    },

    // 监听文件变化并重新构建
    extraWatchFiles: [
        '.vuepress/config.js',
        '.vuepress/config/head.js',
        '.vuepress/config/htmlModules.js',
        '.vuepress/config/nav.js',
        '.vuepress/config/plugins.js',
        '.vuepress/config/themeConfig.js',
        '.vuepress/config/zh/nav.js',
    ],

    locales: {
        '/': {
            lang: 'en-US',
            title: "PicImageSearch",
            description: '✨ Reverse Image Search Aggregator ✨',
        },
        '/zh/': {
            lang: 'zh-CN',
            title: "PicImageSearch",
            description: '✨ 聚合识图引擎 用于以图搜源 ✨',
        }
    }
}
