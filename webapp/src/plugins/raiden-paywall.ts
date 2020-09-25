import _Vue from 'vue';
//import Vuex, {StoreOptions} from 'vuex'
import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse, AxiosError } from "axios";
//import Store from 'vuex';
//import axiosRetry from "axios-retry";
import {Address, BigNumberC} from "raiden-ts";



//function is_raiden_rejected(error: AxiosError): boolean{
	//return (error.response?.status === 401 && error.response?.data?.identifier);
//}

function is_raiden_payment_required(error: AxiosError): boolean{
	return (error.response?.status === 402 && error.response?.data?.identifier);
}

export enum PaymentState{
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
export interface RaidenPaymentExternal extends RaidenPayment{
	state: PaymentState;
	url: URL;
}

function delay(ms: number) {
    return new Promise( resolve => setTimeout(resolve, ms) );}

export class RaidenPaywallHandler{
	// TODO check correct type
	public axios: AxiosInstance;
	private raiden_dapp_url: URL;
	private _callbacks: {(payment: RaidenPaymentExternal): void;}[];
	
	public constructor (raiden_dapp_url: string, config?: AxiosRequestConfig) {
		this.raiden_dapp_url = new URL(raiden_dapp_url);
		this.axios = axios.create(config);
		this._callbacks = [];
		// we provide an interceptor that handles raiden payment requests!
		this.axios.interceptors.response.use(undefined, this._handle_response_error.bind(this));
		console.log("Initialised Raiden Paywall plugin")
	}

	private add_state(payment: RaidenPayment, state: PaymentState): RaidenPaymentExternal{
		let new_payment = payment as RaidenPaymentExternal;
		new_payment.state = state;
		new_payment.url = new URL(`/#/transfer/${payment.token}/${payment.receiver}/${payment.identifier}?amount=${payment.amount}`, this.raiden_dapp_url)
		return new_payment
	}

	private callback(payment: RaidenPaymentExternal){
		console.log(this._callbacks);
		console.log(payment);
		this._callbacks.forEach(callback => {
			callback(payment)
		});
	}

	public register_callback(callback: (payment: RaidenPaymentExternal) => void){
		this._callbacks.push(callback);

	}
	private async _handle_response_error(error: AxiosError): Promise<any> {
		if (error.response) {
			if (is_raiden_payment_required(error)) {
				console.log(JSON.stringify(error));
				const payment = error.response.data
				this.callback(
					this.add_state(payment, PaymentState.REQUESTED)
				);
				error.config.headers['X-Raiden-Payment-Id'] = payment.identifier;
				let num_requests = 0;
				let last_error = undefined;
				// TODO introduce a sync barrier here, that blocks until 
				// a currently 'processed' payment is finished
				do {
					try{
						num_requests++;
						let response = await this.axios(error.config);
						console.log(response);
						this.callback(
							this.add_state(payment, PaymentState.SUCCESS)
						);
						return response;
					} catch (error){
						last_error = error;
						if (error.response?.status === 401){
							// TODO make poll timings as parameters
							await delay(2000);
							continue;

						}else{
							this.callback(
								this.add_state(payment, PaymentState.FAILED)
							);
							return Promise.reject(error)
						}
					}
				// TODO make max requests parameter
				} while (num_requests <= 60);
				this.callback(
					this.add_state(payment, PaymentState.TIMEOUT)
				);
				return Promise.reject(last_error);
			
			}
		}
		return Promise.reject(error);
	}
}


export function RaidenPaywallPlugin(Vue: typeof _Vue, _options?: any): void {
	// TODO make base url an plugin option
	Vue.prototype.$paywall = new RaidenPaywallHandler('http://localhost:8081');
	Vue.prototype.$http = Vue.prototype.$paywall.axios;
}

declare module 'vue/types/vue' {
  // 3. Declare augmentation for Vue
  interface Vue {
    $paywall: RaidenPaywallHandler;
    $http: AxiosInstance;
    raiden_payment: undefined | RaidenPaymentExternal;
  }
}
