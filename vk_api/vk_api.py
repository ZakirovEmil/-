import sys
import time

import requests
from config import API_URL


def make_requests(method, params):
    str_requests = API_URL.replace('METHOD', method) \
        .replace('PARAMS', params) \
        .replace('TOKEN', TOKEN)
    response = requests.get(str_requests)
    if response.status_code == 200 and 'error' not in response.json():
        return response
    else:
        print(response.json()['error']['error_msg'])
        print(response.status_code, response.reason)
        sys.exit()


def get_user_info(id):
    params = f'user_id={id}'
    return make_requests('users.get', params)


def handle_user(user):
    return f"{user['response'][0]['first_name']} {user['response'][0]['last_name']}"


def get_list_friend():
    params = f'user_id={ID}'
    ids_friends = make_requests("friends.get", params).json()['response']['items']
    for id in ids_friends:
        time.sleep(0.2)
        print(handle_user(get_user_info(id).json()))


def main():
    global ID, TOKEN
    ID = input("Enter ID: ")
    TOKEN = input("Token: ")
    print(get_list_friend())


if __name__ == '__main__':
    main()
