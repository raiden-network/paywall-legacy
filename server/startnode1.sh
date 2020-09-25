#!/bin/sh

./raiden \
--address 0x0DAe4282fe47cbE3cc8c17e90e9a22DF25f577d3 \
--keystore-path /Users/ezdac/Library/Ethereum/keystore \
--password-file ./password1.txt \
--eth-rpc-endpoint http://parity.goerli.ethnodes.brainbot.com:8545 \
--network-id 5 \
--environment-type development \
--accept-disclaimer \
--api-address 127.0.0.1:5001 \
--matrix-server https://transport.demo001.env.raiden.network \
--console
