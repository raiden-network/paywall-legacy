<template>
  <div>
    <AppHeader />
    <!-- <PaywalledArticle :article="article" /> -->
    <router-view></router-view>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import AppHeader from './components/AppHeader.vue';
import PaywalledArticle from './components/PaywalledArticle.vue';

@Component({
  components: {
    AppHeader,
    PaywalledArticle,
  },
})
export default class App extends Vue {
  // article: Article = {
  //   id: 1,
  //   title: 'Raiden Pulse #13: News from July and August',
  //   description:
  //     'Two more months have passed by and it’s time for a new bi-monthly summary of all things Raiden',
  //   preview:
  //     'Two more months have passed by and it’s time for a new bi-monthly summary of all things Raiden: overall development progress, product updates, (virtual) event participation and all the other stuff that we’ve been up to in July and August. The overarching focus of July was our participation in the Great Reddit Scaling Bake-Off. In August, the main focus has been on some maintenance work and continuing the implementation of WebRTC for the transport layer in the Raiden python client. The light client team is still working towards reaching parity with the Alderaan release. Let’s dig in!',
  //   date: '2020-09-03',
  //   imageUrl: 'https://miro.medium.com/max/3836/1*UBQGJ9Z1Z8Ib25AqNx7LEQ.png',
  // };
}
</script>

<style></style>
