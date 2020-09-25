import Vue from 'vue'
import App from './App.vue'
import BlockUI from 'vue-blockui'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faSpinner, faHourglassEnd } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

import {RaidenPaywallPlugin} from './plugins/raiden-paywall'


library.add(faSpinner)
Vue.config.productionTip = false

Vue.use(RaidenPaywallPlugin)
Vue.use(BlockUI)
Vue.component('font-awesome-icon', FontAwesomeIcon)

new Vue({
  render: h => h(App),
}).$mount('#app')
