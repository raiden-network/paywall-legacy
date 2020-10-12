<template>
  <div class="page-wrapper">Home</div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

@Component
export default class Home extends Vue {}
</script>

<style scoped lang="scss">
@import '@/scss/dimensions';
@import '@/scss/colors';

.page-wrapper {
  max-width: $page-max-width;
  margin: auto;
  padding: $page-padding;
}
</style>
