#raiden-paywall


1) Install Raiden
Raiden version `1.1.1`

2) Install the server:

```shell
make install-dev
```

3) Start the Raiden node first

```shell
raiden \
--address <node-hex-address> \
--keystore-path <path-to-keystore> \
--password-file <path-to-password-file> \
--config-file config-dev.toml
```

4) Then start the WSGI server:

```shell
make start-server
```

It is assumed, that the Raiden node is connected to the token network `0xC563388e2e2fdD422166eD5E76971D11eD37A466 `on the Goerli testnet.




## Paywall API

The Raiden-Paywall is provided as a Flask-extension.
Configuration is specified in a configuration file, e.g. `defaults.cfg`.
This is a simple file with Python syntax, where following configuration 
parameters are available:

```python
RD_TOKEN_ADDRESS = "0xC563388e2e2fdD422166eD5E76971D11eD37A466"  # Token address of the token to receive paywall payments
RD_TOKEN_DECIMALS = 18  # Token decimals of the corresponding RD_TOKEN_ADDRESS, used to convert the relative amount to absolute
RD_DEFAULT_TIMEOUT = "10mins"  # how long the server waits for a payment after a payment request is sent
RD_DEFAULT_AMOUNT = 0.001  # DEPRECATED - has no effect and will be deprecated
RD_API_ENDPOINT = 'http://localhost:5002'  # the API endpoint of the Raiden node that receives paywall payments
RD_NETWORK_ID = 5  # Network id - should correspond to the Network the Raiden node is running on. Currently only 5 (GOERLI) supported
```

The flask application has then to be started with the environment `variable RAIDEN_PAYWALL_SETTINGS` set to the configuration file path.



```python
from flask import Flask
from flask_raiden import RaidenPaywall

app = Flask(__name__)
paywall = RaidenPaywall(app)

```

The Paywall API provides a very simple interface, that is complying with flask's *per-request*
architecture:


``` python

@app.route('/compute/<computations>')
def get_expensive_stuff(computations):
    # here we could observe the request and calculate the amount to pay based on request data
    computations = int(computations)
    # this is the base amount!
    paywall.amount += 0.0001

    # now we also add dynamic pricing based on the request param!
    paywall.amount += 0.000001 * computations

    # We want to be able to have control over when the paywall is checked.
    if not paywall.check_payment():
        return paywall.preview(f'If you pay, this would compute {computations} rounds of computations!')
    # Because then we could price heavy computation, before 
    # actually having to do the compuation
    for _ in range(computations):
        pr = 213123
        pr * pr
        pr = pr + 1
    return f"Thank you for paying! Here is the result of your computation: {pr}"
```

Since there is no strict association between a specific request
(within a certain user session), the amount should always be deterministic
for a specific combination of endpoint/request parameters!

E.g. this is a non deterministic endpoint pricing:

```python

import datetime

@app.route('/paytime')
def get_expensive_stuff():
	current_time = datetime.datetime.utcnow()
	paywall.amount = current_time.timestamp() * 0.00001
	if not paywall.check_payment():
		return paywall.preview(f'You know what time it is?')
	return currrent_time
```

