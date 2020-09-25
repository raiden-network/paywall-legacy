import json
import sys


def main():
    data = sys.stdin.read()
    dic = json.loads(data)
    identifier = dic['payment_identifier']
    token_address = dic['token_address']
    amount = dic['amount']
    receiver_address = dic['receiver_address']
    # FIXME amount is hardcoded for now, since the server doesn't care if we pay more
    # in the query param, the comma separated amount is used, not the absolute int value
    url = f'https://localhost:8080/#/transfer/{token_address}/{receiver_address}/{identifier}?amount=0.0000001'
    return url


print(main())
