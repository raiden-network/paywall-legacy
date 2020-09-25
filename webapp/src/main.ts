import Vue from 'vue'
import App from './App.vue'
import {RaidenPaywallPlugin} from './plugins/raiden-paywall'

Vue.config.productionTip = false
Vue.use(RaidenPaywallPlugin)

new Vue({
  render: h => h(App),
}).$mount('#app')
