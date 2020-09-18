import _Vue from 'vue';
import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse, AxiosError } from "axios";
import axiosRetry from "axios-retry";
import {Address, BigNumberC} from "raiden-ts";


//The interceptors handle creating some kind of event for initiating a raiden payment
//They will Queue waiting responses somewhere
//


function is_raiden_rejected(error: AxiosError): boolean{
	if (error.response){
		return (error.response?.status === 401 && error.response?.data?.identifier);
	} else{
		return false;
	}
	
}

function is_raiden_payment_required(error: AxiosError): boolean{
	if (error.response){
		return (error.response?.status === 402 && error.response?.data?.identifier);
	} else{
		return false;
	}

}


interface RaidenPayment {
    token: Address;
    receiver: Address;
    identifier: BigNumberC;
    amount: number;
}

interface PaymentPromisePair {
	payment: RaidenPayment;
	promise: Promise<AxiosResponse>;
}

//function decodeRaidenPayment(payment: any): RaidenPayment {
	//return {
		//identifier: payment.identifier,
		//amount: payment.amount,
		//payment.token_address;
		//payment.receiver_address;
		//payment.timeout;
	//}
//}


export class RaidenPaywallHandler{
	private _dapp_url: URL;
	// TODO check correct type
	private _raiden_requests: PaymentPromisePair[];
	public axios: AxiosInstance;
	
	public constructor (dapp_url_string: string, config?: AxiosRequestConfig) {
		this._dapp_url = new URL(dapp_url_string);
		this._raiden_requests = [];

		this.axios = axios.create(config);
		// we provide an interceptor that handles raiden payment requests!
		this.axios.interceptors.response.use(this._handle_response_success, this._handle_response_error.bind(this));
		// Exponential back-off retry delay between requests
		// TODO make this a config parameter
		// TODO maybe calculate the number of retries from a max wait time?
		// REFACTOR maybe implement long polling server side?
		axiosRetry(this.axios, { retryCondition:is_raiden_rejected ,retryDelay: (_) => {return 1000}, retries: 15});
		console.log("Initialised Raiden Paywall plugin")
	}

	private _handle_response_success(response: AxiosResponse): AxiosResponse{
		// TODO do we need this?
		return response;
	}

	private _handle_response_error(error: AxiosError): any {
		if (error.response) {
			if (is_raiden_payment_required(error)) {
				const payment = error.response.data
				console.log(JSON.stringify(error.config))
				const modified_config = error.config
				modified_config.headers['X-Raiden-Payment-Id'] = payment.identifier;
				const retry_promise = this.axios(modified_config);
				// TODO do deserialization / type checking
				this._raiden_requests.push({payment: payment, promise: retry_promise});
				// XXX can we return a possible succesful Response promise triggered by an error?
				return retry_promise;
			}
		}
		return Promise.reject(error);
	}

	get_payment_url(): URL | undefined{
		// FIXME we only return the first element of the promises now. This implicitly means, 
		// that only the first request will be able to get paid, and all others will time out.
		// TODO the dapp should be able to initiate multiple payments
		const payments = this._raiden_requests.map(({payment}) => payment)
		if (payments){
			const payment = payments[0]
			return new URL(`/#/transfer/${payment.token}/${payment.receiver}/${payment.identifier}?amount=${payment.amount}`, this._dapp_url)
		}
	}
	async wait_for_request_finalization(){
		// should be called when all requests for some logical unit (e.g. whole app, component) are asynchronously made
		// once all requests got a reponse, this will check which one of them are still "waiting" for payment
		// triggers emitting an event that causes user input to pay the payments
		// 1) open tab(?) to raiden wallet payment screen
		// 2) show vue loadscreen element informing that the app is waiting
		await Promise.all(this._raiden_requests.map(({promise}) => promise));
	}
}

export function RaidenPaywallPlugin(Vue: typeof _Vue, _options?: any): void {
  Vue.prototype.$paywall = new RaidenPaywallHandler('http://localhost:8081');
  Vue.prototype.$http = Vue.prototype.$paywall.axios;
}

declare module 'vue/types/vue' {
  // 3. Declare augmentation for Vue
  interface Vue {
    $paywall: RaidenPaywallHandler;
    $http: AxiosInstance;
  }
}
