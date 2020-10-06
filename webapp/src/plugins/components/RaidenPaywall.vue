<template>
  <div v-if="showPopup">
    <BlockUI>
      <div v-if="requested">
        <font-awesome-icon icon="spinner" />
        <p>
          This page contains paywalled content. Please make a
          <a
            :href="raiden_payment.url"
            target="_blank"
            rel="noopener noreferrer"
            >Raiden payment</a
          >
          to the content provider in order to use this page.
        </p>
      </div>
      <div v-else-if="timeout">
        <font-awesome-icon icon="hourglass-end" />
        <p>
          The Raiden payment timed out. Please reload the page and make required
          payments.
        </p>
      </div>
    </BlockUI>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { PaymentState } from '../raiden-paywall';

@Component
export default class RaidenPaywall extends Vue {
  created() {
    this.$paywall.register_callback((payment) => this.handlePayment(payment));
  }

  get requested() {
    return this.raiden_payment?.state === PaymentState.REQUESTED;
  }

  get timeout() {
    return this.raiden_payment?.state === PaymentState.TIMEOUT;
  }

  get success() {
    return this.raiden_payment?.state === PaymentState.SUCCESS;
  }

  get showPopup() {
    if (!this.raiden_payment) {
      return false;
    }
    return !this.success;
  }

  data() {
    return {
      msg: 'RaidenPayment required',
      raiden_payment: undefined,
    };
  }

  handlePayment(payment: RaidenPaymentExternal): void {
    // here the plugin vue part will go!
    switch (payment.state) {
      case PaymentState.REQUESTED:
        this.raiden_payment = payment;
        break;
      case PaymentState.SUCCESS:
        if (this.raiden_payment?.identifier === payment.identifier) {
          this.raiden_payment = payment;
          console.log(`Payment successful: ${payment}`);
        } else {
          console.warn('Payment successful, but other payment was waited on');
        }
        break;
      case PaymentState.FAILED:
        break;
      case PaymentState.TIMEOUT:
        this.raiden_payment = payment;
        break;
      default:
        break;
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
/* Define an animation behavior */
@keyframes spinner {
  to {
    transform: rotate(360deg);
  }
}
/* This is the class name given by the Font Awesome component when icon contains 'spinner' */
.fa-spinner {
  /* Apply 'spinner' keyframes looping once every second (1s)  */
  animation: spinner 1s linear infinite;
}

h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
