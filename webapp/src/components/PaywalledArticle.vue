<template>
  <div class="page-wrapper">
    <article class="article" :class="{ 'article--full': content }">
      <h1 class="article__title">{{ article.title }}</h1>
      <div class="article__info">
        <img
          class="article__author-image"
          alt="Image of author"
          src="../assets/icons/raiden.png"
        />
        <div class="article__publication-info">
          <span class="article__author">Raiden Network</span>
          <span class="article__date">{{ article.date | formatDate}}</span>
        </div>
      </div>
      <img
        class="article__image"
        alt="Image for article"
        :src="article.imageUrl"
      />
      <div v-if="content" v-html="content" class="article__content"></div>
      <div v-else class="article__content">
        <p>{{ article.preview }}</p>
      </div>
    </article>

    <RaidenPaywall />
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import { Article } from '../model/types';

@Component({
  filters: {
    formatDate: function (dateString: string) {
      const date = new Date(dateString);
      const options: any = { month: 'short', day: 'numeric' };
      if (date.getFullYear() !== new Date().getFullYear()) {
        options.year = 'numeric';
      }
      return date.toLocaleDateString(undefined, options);
    },
  },
})
export default class PaywalledArticle extends Vue {
  @Prop() article!: Article;

  content = '';

  async mounted() {
    const response = await this.$http.get('http://localhost:5000');
    this.content = response.data;
  }
}
</script>

<style scoped lang="scss">
@import '@/scss/dimensions';
@import '@/scss/colors';

.page-wrapper {
  max-width: $page-max-width;
  margin: auto;
}

.article {
  padding: $page-padding;
  margin-top: 65px;

  &--full {
    margin-bottom: 732px;
  }

  &__title {
    font-size: 48px;
    line-height: 58px;
    font-weight: 700;
    margin: 0;
  }

  &__info {
    display: flex;
    flex-direction: row;
    align-content: stretch;
    align-items: stretch;
    margin-top: 16px;
  }

  &__author-image {
    height: 32px;
    margin-right: 8px;
  }

  &__publication-info {
    font-size: 12px;
    line-height: 14px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;

  }

  &__author {
    color: $primary;
    font-weight: 500;
  }

  &__image {
    display: block;
    width: 100%;
    margin: 32px 0 0 0;
  }

  &__content {
    font-size: 21px;
    line-height: 32px;

    p {
      margin: 32px 0 0 0;
    }
  }
}
</style>
