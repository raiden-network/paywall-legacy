import Vue from 'vue';
import VueRouter from 'vue-router';
import App from './App.vue';
import Home from './components/Home.vue';
import PaywalledArticle from './components/PaywalledArticle.vue';
import './main.scss';

import {
  RaidenPaywallPlugin,
  RaidenPaywallOptions,
} from './plugins/raiden-paywall';

Vue.config.productionTip = false;

Vue.use(VueRouter);

const router = new VueRouter({
  routes: [
    { path: '/article/:id', component: PaywalledArticle },
    { path: '*', component: Home },
  ],
}); // TODO redirect for * to home page

const raidenOptions = {
  raidenUrl: new URL('http://lightclient.raiden.network/staging/'),
  pollInitialWaitTime: 10_000,
  pollInterval: 3_000,
  pollMaxWaitTime: 120_000,
} as RaidenPaywallOptions;

Vue.use(RaidenPaywallPlugin, raidenOptions);

new Vue({
  render: (h) => h(App),
  router: router,
}).$mount('#app');
