<template>
  <div>
    <img class="hero" alt="Raiden banner" src="../assets/images/hero.png" />
    <div class="page-wrapper">
      <div v-if="articles.length > 0" class="article article--highlighted">
        <router-link
          class="article__image-link"
          :to="{ name: 'article', params: { id: articles[0].id } }"
        >
          <img
            class="article__image"
            alt="Image for article"
            :src="articles[0].image_url"
          />
        </router-link>
        <div class="article__content">
          <h3 class="article__title">
            <router-link
              class="article__text-link"
              :to="{ name: 'article', params: { id: articles[0].id } }"
            >
              {{ articles[0].title }}
            </router-link>
          </h3>
          <div class="article__description">
            {{ articles[0].description }}
          </div>
          <div class="article__info">
            <img
              class="article__author-image"
              alt="Image of author"
              src="../assets/images/raiden.png"
            />
            <div class="article__publication-info">
              <span class="article__author">Raiden Network</span>
              <span class="article__date">{{
                articles[0].date | formatDate
              }}</span>
            </div>
          </div>
        </div>
      </div>

      <hr class="divider" />

      <div class="article-wrapper">
        <div
          class="article"
          v-for="article in articles.slice(1)"
          :key="article.id"
        >
          <router-link
            class="article__image-link"
            :to="{ name: 'article', params: { id: article.id } }"
          >
            <img
              class="article__image"
              alt="Image for article"
              :src="article.image_url"
            />
          </router-link>
          <div class="article__content">
            <h3 class="article__title">
              <router-link
                class="article__text-link"
                :to="{ name: 'article', params: { id: article.id } }"
              >
                {{ article.title }}
              </router-link>
            </h3>
            <div class="article__description">
              {{ article.description }}
            </div>
            <div class="article__info">
              <img
                class="article__author-image"
                alt="Image of author"
                src="../assets/images/raiden.png"
              />
              <div class="article__publication-info">
                <span class="article__author">Raiden Network</span>
                <span class="article__date">
                  {{ article.date | formatDate }}
                </span>
              </div>
            </div>
          </div>
        </div>
        <div v-if="articles.length % 3 === 0" class="article">
          <!-- 
            This div is a mock to have the correct gap between elements when wrapped
            due to limitations in flexbox
          -->
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { Article } from '../model/types';

@Component
export default class Home extends Vue {
  articles: Article[] = [];

  async created() {
    const response = await this.$http.get(`${process.env.VUE_APP_CONTENT_BASE_URL}`);
    this.articles = response.data;
  }
}
</script>

<style scoped lang="scss">
@import '@/scss/dimensions';
@import '@/scss/colors';

.hero {
  width: 100%;
  display: block;
}

.page-wrapper {
  max-width: $page-max-width;
  margin: auto;
  padding: $page-padding;
}

.divider {
  width: 100%;
  margin: 24px 0 0 0;
  border: none;
  border-top: 1px solid $black;
}

.article-wrapper {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  flex-wrap: wrap;
  margin-bottom: 60vh;
}

.article {
  width: 32%;
  margin-top: 24px;

  @media screen and (max-width: 599px) {
    width: 100%;
  }

  &--highlighted {
    width: 100%;
    margin-top: 48px;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-content: flex-start;
    align-items: flex-start;

    @media screen and (max-width: 839px) {
      display: flex;
      flex-direction: column;
    }
  }

  &__image-link {
    width: 100%;
  }

  &--highlighted &__image-link {
    width: 66%;

    @media screen and (max-width: 839px) {
      width: 100%;
    }
  }

  &__image {
    display: block;
    width: 100%;
  }

  &__content {
    display: flex;
    flex-direction: column;
    margin-top: 28px;

    & > *:not(:last-child) {
      margin-bottom: 16px;
    }
  }

  &--highlighted &__content {
    width: 32%;

    @media screen and (max-width: 839px) {
      width: 100%;
    }
  }

  &__title {
    font-weight: 700;
    font-size: 32px;
    line-height: 38px;
    margin: 0;
  }

  &__text-link {
    text-decoration: none;
    color: $black;

    &:hover {
      color: $hovered-link-grey;
    }

    &:active {
      color: $active-link-grey;
    }
  }

  &__description {
    font-size: 16px;
    line-height: 22px;
  }

  &__info {
    display: flex;
    flex-direction: row;
    align-content: stretch;
    align-items: stretch;
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
}
</style>
