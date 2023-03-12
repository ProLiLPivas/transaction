import requests

import config


def request_transaction(user_id: int, recipient: str, money: float):
    resp = requests.post(
        f'http://127.0.0.1:8000/remittance',
        params=(('user_id', user_id),),
        json={
            'recipient_name': recipient,
            'amount': money
        }
    )
    print(resp)


def get_user(user_id):
    resp = requests.get(
        f'http://127.0.0.1:8000/user',
        params=(('user_id', user_id),),
    )
    return resp.json()
