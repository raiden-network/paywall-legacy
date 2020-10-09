import Vue from 'vue';
import App from './App.vue';
import './main.scss';

import {
  RaidenPaywallPlugin,
  RaidenPaywallOptions,
} from './plugins/raiden-paywall';

Vue.config.productionTip = false;

const raidenOptions = {
  raidenUrl: new URL('http://lightclient.raiden.network/staging/'),
  pollInitialWaitTime: 10_000,
  pollInterval: 3_000,
  pollMaxWaitTime: 120_000,
} as RaidenPaywallOptions;

Vue.use(RaidenPaywallPlugin, raidenOptions);

new Vue({
  render: h => h(App),
}).$mount('#app');
