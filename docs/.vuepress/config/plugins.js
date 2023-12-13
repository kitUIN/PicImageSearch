module.exports = [
    // [require('./plugins/love-me'), { // 鼠标点击爱心特效
    //   color: '#11a8cd', // 爱心颜色，默认随机色
    //   excludeClassName: 'theme-vdoing-content' // 要排除元素的 class, 默认空''
    // }],

    ['fulltext-search'], // 全文搜索
    [
        'vuepress-plugin-comment-plus',
        {
            choosen: 'waline',
            // options 选项中的所有参数，会传给 Waline 的配置
            options: {
                el: '#valine-vuepress-comment',
                serverURL: 'https://kituin-comments.vercel.app/', //  例如 "https://***.vercel.app/"
                path: '<%- frontmatter.commentid || frontmatter.permalink %>',
                emoji: [
                    'https://cdn.jsdelivr.net/gh/walinejs/emojis@1.0.0/weibo',
                    'https://cdn.jsdelivr.net/gh/walinejs/emojis@1.0.0/bilibili',
                ],
                placeholder: "请留言"
            }
        }
    ],
    // ['thirdparty-search', { // 可以添加第三方搜索链接的搜索框（原官方搜索框的参数仍可用）
    //   thirdparty: [// 可选，默认 []
    //     {
    //       title: '在GitHub中搜索',
    //       frontUrl: 'https://github.com/search?q=', // 搜索链接的前面部分
    //       behindUrl: '' // 搜索链接的后面部分，可选，默认 ''
    //     },
    //     {
    //       title: '在npm中搜索',
    //       frontUrl: 'https://www.npmjs.com/search?q=',
    //     },
    //     {
    //       title: '在Bing中搜索',
    //       frontUrl: 'https://cn.bing.com/search?q='
    //     }
    //   ]
    // }],


    ['one-click-copy', { // 代码块复制按钮
        copySelector: ['div[class*="language-"] pre', 'div[class*="aside-code"] aside'], // String or Array
        copyMessage: '复制成功', // default is 'Copy successfully and then paste it for use.'
        duration: 1000, // prompt message display time.
        showInMobile: false // whether to display on the mobile side, default: false.
    }],
    ['demo-block', { // demo 演示模块 https://github.com/xiguaxigua/vuepress-plugin-demo-block
        settings: {
            // jsLib: ['http://xxx'], // 在线示例 (jsfiddle, codepen) 中的 js 依赖
            // cssLib: ['http://xxx'], // 在线示例中的 css 依赖
            // vue: 'https://fastly.jsdelivr.net/npm/vue/dist/vue.min.js', // 在线示例中的 vue 依赖
            jsfiddle: false, // 是否显示 jsfiddle 链接
            codepen: true, // 是否显示 codepen 链接
            horizontal: false // 是否展示为横向样式
        }
    }],
    [
        'vuepress-plugin-zooming', // 放大图片
        {
            selector: '.theme-vdoing-content img:not(.no-zoom)',
            options: {
                bgColor: 'rgba(0,0,0,0.6)'
            },
        },
    ],
    [
        '@vuepress/last-updated', // "上次更新"时间格式
        {
            transformer: (timestamp, lang) => {
                const dayjs = require('dayjs') // https://day.js.org/
                return dayjs(timestamp).format('YYYY/MM/DD, HH:mm:ss')
            },
        }
    ]
]
