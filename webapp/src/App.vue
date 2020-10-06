<template>
  <div id="app">
    <img alt="Vue logo" src="./assets/logo.png" />
    <PaywalledContent msg="Welcome to the Raiden Paywall app" />
    <RaidenPaywall msg="Hallo test" />
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import PaywalledContent from './components/PaywalledContent.vue';

@Component({
  components: {
    PaywalledContent,
  },
})
export default class App extends Vue {}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
