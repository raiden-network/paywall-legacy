import _Vue from 'vue';
//import Vuex, {StoreOptions} from 'vuex'
import axios, {
  AxiosInstance,
  AxiosRequestConfig,
  AxiosResponse,
  AxiosError,
} from 'axios';
//import Store from 'vuex';
//import axiosRetry from "axios-retry";
import { Address, BigNumberC } from 'raiden-ts';
import RaidenPaywall from './components/RaidenPaywall.vue';
import BlockUI from 'vue-blockui';

import { library } from '@fortawesome/fontawesome-svg-core';
import { faSpinner, faHourglassEnd } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';

//function is_raiden_rejected(error: AxiosError): boolean{
//return (error.response?.status === 401 && error.response?.data?.identifier);
//}

function is_raiden_payment_required(error: AxiosError): boolean {
  return error.response?.status === 402 && error.response?.data?.identifier;
}

export enum PaymentState {
  SUCCESS = 'SUCCESS',
  FAILED = 'FAILED',
  REQUESTED = 'REQUESTED',
  TIMEOUT = 'TIMEOUT',
}

interface RaidenPayment {
  token: Address;
  receiver: Address;
  identifier: BigNumberC;
  amount: number;
}

// TODO rename this one to RaidenPayment
export interface RaidenPaymentExternal extends RaidenPayment {
  state: PaymentState;
  url: URL;
}

function delay(ms: number) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

export class RaidenPaywallHandler {
  // TODO check correct type
  public axios: AxiosInstance;
  private raiden_dapp_url: URL;
  private _callbacks: { (payment: RaidenPaymentExternal): void }[];
  private _pollInitialWaitTime: number;
  private _pollMaxWaitTime: number;
  private _pollInterval: number;

  public constructor(
    options: RaidenPaywallOptions,
    config?: AxiosRequestConfig,
  ) {
    this.raiden_dapp_url = options.raidenUrl;
    this._pollInterval = options.pollInterval || 2_000;
    this._pollMaxWaitTime = options.pollMaxWaitTime || 120_000;
    this._pollInitialWaitTime = options.pollInitialWaitTime || 0;

    this.axios = axios.create(config);
    this._callbacks = [];
    // we provide an interceptor that handles raiden payment requests!
    this.axios.interceptors.response.use(
      undefined,
      this._handle_response_error.bind(this),
    );
    console.log('Initialised Raiden Paywall plugin');
  }

  private add_state(
    payment: RaidenPayment,
    state: PaymentState,
  ): RaidenPaymentExternal {
    let new_payment = payment as RaidenPaymentExternal;
    new_payment.state = state;
    new_payment.url = new URL(
      `#/transfer/${payment.token}/${payment.receiver}?identifier=${payment.identifier}&amount=${payment.amount}`,
      this.raiden_dapp_url,
    );
    return new_payment;
  }

  private callback(payment: RaidenPaymentExternal) {
    this._callbacks.forEach((callback) => {
      callback(payment);
    });
  }

  public register_callback(callback: (payment: RaidenPaymentExternal) => void) {
    this._callbacks.push(callback);
  }

  private poll_timeout_reached(
    start_poll_time: Date,
    payment_timeout: Date,
  ): boolean {
    const time_now = new Date().getTime().valueOf();
    console.log(start_poll_time.getTime(), payment_timeout.getTime());
    return (
      time_now > payment_timeout.getTime().valueOf() ||
      time_now - start_poll_time.getTime().valueOf() > this._pollMaxWaitTime
    );
  }

  private async _handle_response_error(error: AxiosError): Promise<any> {
    if (error.response) {
      if (is_raiden_payment_required(error)) {
        const payment = error.response.data;
        this.callback(this.add_state(payment, PaymentState.REQUESTED));
        error.config.headers['X-Raiden-Payment-Id'] = payment.identifier;
        let last_error = undefined;
        const started_time = new Date();
        // TODO introduce a sync barrier here, that blocks until
        // a currently 'processed' payment is finished
        let num_requests = 0;
        do {
          try {
            let response = await this.axios(error.config);
            this.callback(this.add_state(payment, PaymentState.SUCCESS));
            return response;
          } catch (error) {
            last_error = error;
            if (error.response?.status === 401) {
              num_requests++;
              if (num_requests == 1) {
                await delay(this._pollInitialWaitTime);
              } else {
                await delay(this._pollInterval);
              }
              continue;
            } else {
              this.callback(this.add_state(payment, PaymentState.FAILED));
              return Promise.reject(error);
            }
          }
        } while (
          !this.poll_timeout_reached(started_time, new Date(payment.timeout))
        );
        this.callback(this.add_state(payment, PaymentState.TIMEOUT));
        return Promise.reject(last_error);
      }
    }
    return Promise.reject(error);
  }
}

// Timedeltas:
//var eventStartTime = new Date(event.startTime);
//var eventEndTime = new Date(event.endTime);
//var duration = eventEndTime.valueOf() - eventStartTime.valueOf();

export interface RaidenPaywallOptions {
  raidenUrl: URL;
  pollInterval?: number;
  pollMaxWaitTime?: number | undefined;
  pollInitialWaitTime?: number | undefined;
}

export function RaidenPaywallPlugin(Vue: typeof _Vue, _options?: any): void {
  library.add(faSpinner, faHourglassEnd);
  Vue.use(BlockUI);
  Vue.component('font-awesome-icon', FontAwesomeIcon);

  const paywall_options = _options as RaidenPaywallOptions;

  Vue.prototype.$paywall = new RaidenPaywallHandler(paywall_options);
  Vue.prototype.$http = Vue.prototype.$paywall.axios;
  Vue.component('RaidenPaywall', RaidenPaywall);
}

declare module 'vue/types/vue' {
  // 3. Declare augmentation for Vue
  interface Vue {
    $paywall: RaidenPaywallHandler;
    $http: AxiosInstance;
    raiden_payment: undefined | RaidenPaymentExternal;
  }
}
