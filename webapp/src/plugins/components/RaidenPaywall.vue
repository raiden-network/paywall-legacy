<template>
  <BlockUI v-if="showPopup">
    <div class="paywall">
      <template v-if="requested">
        <img
          class="paywall__icon"
          alt="Shopping icon"
          src="../../assets/icons/shop.svg"
        />
        <div class="paywall__info">
          <span>
            {{
              message
                ? message
                : 'Please make a Raiden payment to view this page'
            }}
          </span>
          <a
            class="paywall__info-link"
            href="https://docs.raiden.network"
            target="_blank"
          >
            <img
              class="paywall__info-icon"
              alt="Info"
              src="../../assets/icons/info.svg"
            />
          </a>
        </div>
        <a
          class="paywall__button"
          :href="raidenPayment.url"
          target="_blank"
          rel="noopener noreferrer"
        >
          Make Payment
        </a>
      </template>
      <template v-else-if="timeout">
        The Raiden payment timed out. Please reload the page and make the
        required payment.
      </template>
    </div>
  </BlockUI>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';
import { PaymentState, RaidenPaymentExternal } from '../raiden-paywall';

@Component({
  watch: {
    showPopup: function (show: boolean) {
      if (show) {
        document.documentElement.style.overflow = 'hidden';
        return;
      }
      document.documentElement.style.overflow = 'auto';
    },
  },
})
export default class RaidenPaywall extends Vue {
  @Prop() message!: string;

  raidenPayment: RaidenPaymentExternal | null = null;

  created() {
    this.$paywall.register_callback((payment) => this.handlePayment(payment));
  }

  get requested(): boolean {
    return this.raidenPayment?.state === PaymentState.REQUESTED;
  }

  get timeout(): boolean {
    return this.raidenPayment?.state === PaymentState.TIMEOUT;
  }

  get success(): boolean {
    return this.raidenPayment?.state === PaymentState.SUCCESS;
  }

  get showPopup(): boolean {
    if (!this.raidenPayment) {
      return false;
    }
    return !this.success;
  }

  destroyed() {
    document.documentElement.style.overflow = 'auto';
  }

  private handlePayment(payment: RaidenPaymentExternal): void {
    switch (payment.state) {
      case PaymentState.REQUESTED:
        this.raidenPayment = payment;
        break;
      case PaymentState.SUCCESS:
        if (this.raidenPayment?.id === payment.id) {
          this.raidenPayment = payment;
          console.log(`Payment successful: ${payment}`);
        } else {
          console.warn('Payment successful, but other payment was waited on');
        }
        break;
      case PaymentState.FAILED:
        break;
      case PaymentState.TIMEOUT:
        this.raidenPayment = payment;
        break;
      default:
        break;
    }
  }
}
</script>

<style scoped lang="scss">
.loading-container::v-deep {
  div.loading-backdrop {
    background: linear-gradient(
      180deg,
      rgba(255, 255, 255, 0) 50%,
      #000000 95%
    );
    opacity: 1;
  }

  div.loading {
    background-color: #f9f9f9;
    box-shadow: 0px 14px 40px rgba(0, 0, 0, 0.04);
    border-radius: 18px;
    padding: 37px 32px 32px 32px;
    box-sizing: border-box;
    width: 650px;
    @media only screen and (max-width: 670px) {
      width: 90vw;
    }
  }
}

.paywall {
  font-size: 24px;
  line-height: 31px;
  display: flex;
  flex-direction: column;
  align-items: center;
  align-content: center;

  & > *:not(:last-child) {
    margin-bottom: 32px;
  }

  &__icon {
    height: 60px;
  }

  &__button {
    display: block;
    width: 100%;
    max-width: 243px;
    border-radius: 100px;
    padding: 9.5px 16px;
    font-family: 'DM Mono', monospace;
    font-size: 16px;
    line-height: 21px;
    font-weight: 500;
    color: #000000;
    text-decoration: none;
    background-color: #44ddff;

    &:hover {
      background-color: #5ce1ff;
    }

    &:active {
      background-color: #70e5ff;
    }
  }

  &__info {
    display: flex;
    flex-direction: row;
    align-items: center;
    align-content: center;

    & > *:not(:last-child) {
      margin-right: 10px;
    }
  }

  &__info-link {
    line-height: 0;
  }

  &__info-icon {
    height: 24px;
  }
}
</style>
