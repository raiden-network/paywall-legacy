import _Vue from 'vue';
//import Vuex, {StoreOptions} from 'vuex'
import axios, { AxiosInstance, AxiosRequestConfig, AxiosError } from 'axios';
//import Store from 'vuex';
//import axiosRetry from "axios-retry";
import { Address } from 'raiden-ts';
import RaidenPaywall from './components/RaidenPaywall.vue';
import BlockUI from 'vue-blockui';

//function is_raiden_rejected(error: AxiosError): boolean{
//return (error.response?.status === 401 && error.response?.data?.identifier);
//}

function isRaidenPaymentRequired(
  error: AxiosError,
): error is AxiosError<PaywallResponse> {
  return error.response?.status === 402 && error.response?.data?.payment?.id;
}

export enum PaymentState {
  SUCCESS = 'SUCCESS',
  FAILED = 'FAILED',
  REQUESTED = 'REQUESTED',
  TIMEOUT = 'TIMEOUT',
}

interface Participant {
  address: Address;
  network_id: number;
}

interface Token {
  address: Address;
  decimals: number;
  network_id: number;
}

interface RaidenPreview {
  date: Date;
  description: string;
  id: string;
  image_url: URL;
  preview: string;
  title: string;
}

interface RaidenPaymentResponse {
  token: Token;
  receiver: Participant;
  id: string;
  amount: string;
  claimed: boolean;
  timeout: Date;
}

interface PaywallResponse {
  payment: RaidenPaymentResponse;
  preview: RaidenPreview;
}

export interface RaidenPayment extends RaidenPaymentResponse {
  state: PaymentState;
  url: URL;
}

function delay(ms: number) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

export class RaidenPaywallHandler {
  public axios: AxiosInstance;
  // TODO change type
  public currentPreview: RaidenPreview | undefined;
  private _raidenDappUrl: URL;
  private _callbacks: ((payment: RaidenPayment) => void)[];
  private _pollInitialWaitTime: number;
  private _pollMaxWaitTime: number;
  private _pollInterval: number;

  public constructor(
    options: RaidenPaywallOptions,
    config?: AxiosRequestConfig,
  ) {
    this._raidenDappUrl = options.raidenUrl;
    this._pollInterval = options.pollInterval || 2_000;
    this._pollMaxWaitTime = options.pollMaxWaitTime || 120_000;
    this._pollInitialWaitTime = options.pollInitialWaitTime || 0;

    this.axios = axios.create(config);
    this._callbacks = [];
    // we provide an interceptor that handles raiden payment requests!
    this.axios.interceptors.response.use(undefined, (error) =>
      this._handleResponseError(error),
    );
    console.log('Initialised Raiden Paywall plugin');
  }

  public registerCallback(callback: (payment: RaidenPayment) => void) {
    this._callbacks.push(callback);
  }

  private addState(
    payment: RaidenPaymentResponse,
    state: PaymentState,
  ): RaidenPayment {
    const url = new URL(
      `#/transfer/${payment.token.address}/${payment.receiver.address}?identifier=${payment.id}&amount=${payment.amount}`,
      this._raidenDappUrl,
    );
    return {
      ...payment,
      state: state,
      url: url,
    };
  }

  private _callback(payment: RaidenPayment) {
    this._callbacks.forEach((callback) => {
      callback(payment);
    });
  }

  private _pollTimeoutReached(
    startPollTime: Date,
    paymentTimeout: Date,
  ): boolean {
    const timeNow = new Date().getTime().valueOf();
    return (
      timeNow > paymentTimeout.getTime().valueOf() ||
      timeNow - startPollTime.getTime().valueOf() > this._pollMaxWaitTime
    );
  }

  private async _handleResponseError(error: AxiosError): Promise<any> {
    if (!(error.response && isRaidenPaymentRequired(error))) {
      return Promise.reject(error);
    }

    const { payment, preview } = error.response.data;
    this.currentPreview = preview;
    this._callback(this.addState(payment, PaymentState.REQUESTED));
    error.config.headers['X-Raiden-Payment-Id'] = payment.id;
    let lastError = undefined;
    const startedTime = new Date();
    // TODO introduce a sync barrier here, that blocks until
    // a currently 'processed' payment is finished
    let numRequests = 0;
    do {
      try {
        let response = await this.axios(error.config);
        this._callback(this.addState(payment, PaymentState.SUCCESS));
        return response;
      } catch (error) {
        lastError = error;
        if (error.response?.status === 401) {
          numRequests++;
          if (numRequests == 1) {
            await delay(this._pollInitialWaitTime);
          } else {
            await delay(this._pollInterval);
          }
          continue;
        } else {
          this._callback(this.addState(payment, PaymentState.FAILED));
          return Promise.reject(error);
        }
      }
    } while (!this._pollTimeoutReached(startedTime, new Date(payment.timeout)));
    this._callback(this.addState(payment, PaymentState.TIMEOUT));
    return Promise.reject(lastError);
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
  Vue.use(BlockUI);

  const paywallOptions = _options as RaidenPaywallOptions;

  Vue.prototype.$paywall = new RaidenPaywallHandler(paywallOptions);
  Vue.prototype.$http = Vue.prototype.$paywall.axios;
  Vue.component('RaidenPaywall', RaidenPaywall);
}

declare module 'vue/types/vue' {
  interface Vue {
    $paywall: RaidenPaywallHandler;
    $http: AxiosInstance;
  }
}
