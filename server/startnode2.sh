#!/bin/sh

./raiden \
--address 0x7EBCB45883298624C7F721065C8BB61e6Dee0278 \
--keystore-path /Users/ezdac/Library/Ethereum/keystore \
--password-file ./password1.txt \
--eth-rpc-endpoint http://parity.goerli.ethnodes.brainbot.com:8545 \
--network-id 5 \
--environment-type development \
--accept-disclaimer \
--api-address 127.0.0.1:5002
