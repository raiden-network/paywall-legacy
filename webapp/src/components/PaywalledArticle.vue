<template>
  <div class="page-wrapper">
    <article
      v-if="article"
      class="article"
      :class="{ 'article--full': content }"
    >
      <h1 class="article__title">{{ article.title }}</h1>
      <div class="article__info">
        <img
          class="article__author-image"
          alt="Image of author"
          src="../assets/images/raiden.png"
        />
        <div class="article__publication-info">
          <span class="article__author">Raiden Network</span>
          <span class="article__date">{{ article.date | formatDate }}</span>
        </div>
      </div>
      <img
        class="article__image"
        alt="Image for article"
        :src="article.image_url"
      />
      <div v-if="content" v-html="content" class="article__content"></div>
      <div v-else class="article__content">
        <p>{{ article.preview }}</p>
      </div>
    </article>

    <RaidenPaywall
      :message="'Please make a Raiden payment to read this article'"
      @preview="article = $event"
    />
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { Article } from '../model/types';

@Component<PaywalledArticle>({
  watch: {
    '$route.params.id': function () {
      this.loadArticle();
    },
  },
})
export default class PaywalledArticle extends Vue {
  article: Article | null = null;
  content = '';

  async mounted() {
    this.loadArticle();
  }

  private async loadArticle() {
    try {
      const articleResponse = await this.$http.get(
				`${process.env.VUE_APP_CONTENT_BASE_URL}${this.$route.params.id}`
      );
      this.content = articleResponse.data;
    } catch (error) {
      if (error.response.status === 404) {
        this.$router.replace('/');
      }
    }
  }
}
</script>

<style scoped lang="scss">
@import '@/scss/dimensions';
@import '@/scss/colors';

.page-wrapper {
  max-width: $page-max-width;
  margin: auto;
  padding: $page-padding;
}

.article {
  margin-top: 65px;

  &--full {
    margin-bottom: 60vh;
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

    &::v-deep {
      p {
        margin: 32px 0 0 0;
      }

      h2,
      h3 {
        margin: 60px 0 0 0;
        font-size: 36px;
        line-height: 43px;
        font-weight: 700;
      }

      h4 {
        margin: 48px 0 0 0;
        font-size: 24px;
        line-height: 31px;
        font-weight: 700;
      }

      ul {
        margin: 32px 0 0 0;
        list-style: '- ' outside;
        padding: 0 0 0 16px;
      }

      li {
        margin: 16px 0 0 0;
      }

      a {
        text-decoration: underline;
        color: $black;

        &:hover {
          color: $hovered-link-grey;
        }

        &:active {
          color: $active-link-grey;
        }
      }

      strong {
        font-weight: 700;
      }

      em {
        font-style: italic;
      }

      hr {
        margin: 60px auto;
        border: none;
        border-top: 5px dotted $black;
        width: 48px;
      }
    }
  }
}
</style>
