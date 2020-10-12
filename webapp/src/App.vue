<template>
  <div>
    <AppHeader />
    <router-view></router-view>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import AppHeader from './components/AppHeader.vue';

@Component({
  components: {
    AppHeader,
  },
})
export default class App extends Vue {}
</script>

<style></style>
