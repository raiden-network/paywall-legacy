<template>
  <div class="page-wrapper">
    <header class="header">
      <router-link class="header__logo header__link" :to="{ name: 'home' }">
        Raiden Pulse
      </router-link>
      <div class="header__links-section">
        <a
          class="header__link"
          href="https://raiden.network/privacy.html"
          target="_blank"
        >
          Imprint
        </a>
        <a
          class="header__link header__link--button"
          href="https://raiden.network/"
          target="_blank"
        >
          Info
        </a>
      </div>
    </header>
  </div>
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator';

@Component
export default class AppHeader extends Vue {}
</script>

<style scoped lang="scss">
@import '@/scss/dimensions';
@import '@/scss/fonts';
@import '@/scss/colors';

.page-wrapper {
  max-width: $page-max-width;
  margin: auto;
  padding: $page-padding;
}

.header {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  align-content: center;
  flex-wrap: wrap;
  min-height: 72px;

  &__logo {
    font-family: $mono-font;
    font-weight: 500;
    font-size: 24px;
    line-height: 31px;
    letter-spacing: -0.04em;
  }

  &__links-section {
    font-size: 16px;
    line-height: 21px;
  }

  &__link {
    color: $black;
    text-decoration: none;

    &:not(:last-child) {
      margin-right: 16px;
    }

    &:hover {
      color: $hovered-link-grey;
    }

    &:active {
      color: $active-link-grey;
    }

    &--button {
      border: 1px solid $black;
      box-sizing: border-box;
      border-radius: 100px;
      padding: 10px 24px;

      &:hover {
        color: $black;
        background-color: $hovered-button-grey;
      }

      &:active {
        color: $black;
        background-color: $active-button-grey;
      }
    }
  }
}
</style>
