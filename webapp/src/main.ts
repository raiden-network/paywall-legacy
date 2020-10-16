import Vue from 'vue';
import VueRouter from 'vue-router';
import App from './App.vue';
import Home from './components/Home.vue';
import PaywalledArticle from './components/PaywalledArticle.vue';
import './filters/formatDate';
import './main.scss';

import {
  RaidenPaywallPlugin,
  RaidenPaywallOptions,
} from './plugins/raiden-paywall';

Vue.config.productionTip = false;

Vue.use(VueRouter);

const router = new VueRouter({
  routes: [
    { path: '/', name: 'home', component: Home },
    { path: '/article/:id', name: 'article', component: PaywalledArticle },
    { path: '*', component: Home },
  ],
});

const raidenOptions: RaidenPaywallOptions = {
  raidenUrl: new URL('http://lightclient.raiden.network/staging/'),
  pollInitialWaitTime: 10_000,
  pollInterval: 3_000,
  pollMaxWaitTime: 120_000,
};

Vue.use(RaidenPaywallPlugin, raidenOptions);

new Vue({
  render: (h) => h(App),
  router: router,
}).$mount('#app');
