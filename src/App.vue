<template>
  <div id="app">
    <img alt="Vue logo" src="./assets/logo.png">
    <RaidenPaywall msg="Welcome to the Raiden Paywall app"/>
		<RaidenPopup msg="Hallo test"/>
  </div>
</template>

<script lang="ts">


import { Component, Vue } from 'vue-property-decorator';
import RaidenPaywall from './components/Paywall.vue';
import RaidenPopup from './components/RaidenPopup.vue';

@Component({
  components: {
		RaidenPaywall,
		RaidenPopup,
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
