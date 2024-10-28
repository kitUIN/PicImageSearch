<template>
  <div class="contributor-list">
    <h2 v-if="title">🎖 {{ title }}</h2>
    <div class="cardListContainer">
      <div class="card-list">
        <template v-for="contributor in processedContributors">
          <a
              :key="contributor.name"
              :href="contributor.link"
              target="_blank"
              class="card-item row-3"
              :style="{
              backgroundColor: contributor.bgColor,
              '--randomColor': contributor.bgColor,
              color: contributor.textColor,
            }"
          >
            <img
                v-if="contributor.avatar"
                :src="contributor.avatar"
                :alt="`Avatar of ${contributor.name}`"
                class="no-zoom"
            />
            <div>
              <p class="name">{{ contributor.name }}</p>
              <p class="desc">{{ contributor.desc }}</p>
            </div>
          </a>
        </template>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ContributorList",
  props: {
    title: {
      type: String,
      default: "Contributors to this project",
    },
    descriptions: {
      type: Object,
      default: () => ({
        NekoAria: "Primary Maintainer of the Project",
        kitUIN: "Project Owner",
        Peloxerat: "Project Contributors",
        lleans: "Project Contributors",
        chinoll: "Project Contributors",
        Nachtalb: "Project Contributors",
      }),
    },
  },
  data() {
    return {
      contributors: [
        {
          name: "NekoAria(Neko Aria)",
          avatar: "https://avatars.githubusercontent.com/u/23137034?v=4",
          link: "https://github.com/NekoAria",
          bgColor: "#d2e4ff",
          textColor: "#001d37",
        },
        {
          name: "kitUIN(Nacho)",
          avatar: "https://avatars.githubusercontent.com/u/68675068?v=4",
          link: "https://github.com/kitUIN",
          bgColor: "#ffd8ec",
          textColor: "#37072a",
        },
        {
          name: "Peloxerat",
          avatar: "https://avatars.githubusercontent.com/u/135450017?v=4",
          link: "https://github.com/Peloxerat",
          bgColor: "#fae287",
          textColor: "#221b00",
        },
        {
          name: "lleans",
          avatar: "https://avatars.githubusercontent.com/u/68429210?v=4",
          link: "https://github.com/lleans",
          bgColor: "#ffdbc9",
          textColor: "#331200",
        },
        {
          name: "chinoll(Chinoll)",
          avatar: "https://avatars.githubusercontent.com/u/22575232?v=4",
          link: "https://github.com/chinoll",
          bgColor: "#ffd9df",
          textColor: "#3a0717",
        },
        {
          name: "Nachtalb",
          avatar: "https://avatars.githubusercontent.com/u/9467802?v=4",
          link: "https://github.com/Nachtalb",
          bgColor: "#ffd9e4",
          textColor: "#39071f",
        },
      ],
    };
  },
  computed: {
    processedContributors() {
      return this.contributors.map((contributor) => ({
        ...contributor,
        desc:
            this.descriptions[contributor.name.split("(")[0]] ||
            "Project Contributors",
      }));
    },
  },
};
</script>
