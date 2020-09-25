#!/bin/sh

./raiden \
--address 0xfc964FBFA4C46Dcaf66D411c13A46863B47960E3 \
--keystore-path /Users/ezdac/Library/Ethereum/keystore \
--password-file ./password1.txt \
--eth-rpc-endpoint http://parity.goerli.ethnodes.brainbot.com:8545 \
--network-id 5 \
--environment-type development \
--accept-disclaimer \
--api-address 127.0.0.1:5003
