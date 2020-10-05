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


