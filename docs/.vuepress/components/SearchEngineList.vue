<template>
  <div class="search-engine-list">
    <h2 v-if="title">🎉 {{ title }}</h2>
    <div class="cardListContainer">
      <div class="card-list">
        <template v-for="engine in engines">
          <a
              :key="engine.name"
              :href="engine.link"
              target="_blank"
              class="card-item row-3"
              :style="{
              backgroundColor: engine.bgColor,
              '--randomColor': engine.bgColor,
              color: engine.textColor,
            }"
          >
            <img
                v-if="engine.avatar"
                :src="engine.avatar"
                :alt="`Avatar of ${engine.name}`"
                class="no-zoom"
            />
            <div>
              <p class="name">{{ engine.name }}</p>
              <p class="desc">{{ engine.desc }}</p>
            </div>
          </a>
        </template>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "SearchEngineList",
  props: {
    title: {
      type: String,
      default: "",
    },
  },
  data() {
    return {
      engines: [
        {
          name: "Ascii2D",
          desc: "二次元画像詳細検索",
          avatar: "/img/ascii2d.png",
          link: "https://ascii2d.net",
          bgColor: "#9cf1f1",
          textColor: "#002020",
        },
        {
          name: "BaiDu",
          desc: "百度图片",
          avatar: "/img/baidu.png",
          link: "https://image.baidu.com/",
          bgColor: "#e0e0ff",
          textColor: "#11144b",
        },
        {
          name: "Bing",
          desc: "Bing Images",
          avatar: "/img/bing.png",
          link: "https://www.bing.com/images",
          bgColor: "#d7e2ff",
          textColor: "#001b3f",
        },
        {
          name: "Copyseeker",
          desc: "The Best Free AI Powered Reverse Image Search Like No Other",
          avatar: "/img/copyseeker.png",
          link: "https://copyseeker.net",
          bgColor: "#e0e0ff",
          textColor: "#11144b",
        },
        {
          name: "E-hentai",
          desc: "E-Hentai Galleries",
          avatar: "/img/e-hentai.png",
          link: "https://e-hentai.org",
          bgColor: "#ffdad7",
          textColor: "#3b0909",
        },
        {
          name: "Google",
          desc: "Google Images",
          avatar: "/img/google.png",
          link: "https://www.google.com/imghp",
          bgColor: "#9df0f8",
          textColor: "#002022",
        },
        {
          name: "Iqdb",
          desc: "Multi-service image search",
          avatar: "/img/iqdb.png",
          link: "https://iqdb.org",
          bgColor: "#ffdbcf",
          textColor: "#380d00",
        },
        {
          name: "SauceNAO",
          desc: "SauceNAO Reverse Image Search",
          avatar: "/img/saucenao.png",
          link: "https://saucenao.com",
          bgColor: "#ffdadc",
          textColor: "#3b0712",
        },
        {
          name: "TraceMoe",
          desc: "Anime Scene Search Engine",
          avatar: "/img/tracemoe.png",
          link: "https://trace.moe",
          bgColor: "#dfe0ff",
          textColor: "#0e154b",
        },
        {
          name: "Yandex",
          desc: "Yandex Images",
          avatar: "/img/yandex.png",
          link: "https://yandex.com/images",
          bgColor: "#ffdad3",
          textColor: "#3a0a03",
        },
      ],
    };
  },
};
</script>
