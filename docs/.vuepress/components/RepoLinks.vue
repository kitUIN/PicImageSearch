<template>
  <div>
    <p align="center">
      <a
          href="https://raw.githubusercontent.com/kitUIN/PicImageSearch/master/LICENSE"
      >
        <img
            src="https://img.shields.io/github/license/kitUIN/PicImageSearch"
            alt="license"
        />
      </a>
      <a href="https://pypi.python.org/pypi/PicImageSearch">
        <img src="https://img.shields.io/pypi/v/PicImageSearch" alt="pypi"/>
      </a>
      <img src="https://img.shields.io/badge/python-3.9+-blue" alt="python"/>
      <a href="https://github.com/kitUIN/PicImageSearch/releases">
        <img
            src="https://img.shields.io/github/v/release/kitUIN/PicImageSearch"
            alt="release"
        />
      </a>
      <a href="https://github.com/kitUIN/PicImageSearch/issues">
        <img
            src="https://img.shields.io/github/issues/kitUIN/PicImageSearch"
            alt="release"
        />
      </a>
    </p>
    <p align="center">
      <a href="https://github.com/kitUIN/PicImageSearch/compare/"
      >✅ {{ prText }}</a
      >
      ·
      <a href="https://github.com/kitUIN/PicImageSearch/issues/new"
      >🐛 {{ issueText }}</a
      >
    </p>
  </div>
</template>

<script>
export default {
  name: "RepoLinks",
  props: {
    prText: {
      type: String,
      default: "Submit PR",
    },
    issueText: {
      type: String,
      default: "Submit Issue",
    },
  },
};
</script>
