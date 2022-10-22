import requests
import hashlib
from pystyle import *

def request_api_data(query_char):
    res = requests.get(f'https://api.pwnedpasswords.com/range/{query_char}')
    if res.status_code != 200: raise RuntimeError(f'Error fetching: {res.status_code}, check api and try again')
    return res


def get_password_leaks_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        Write.Print(f'Your password was found {count} times !\n', Colors.rainbow, interval=0.001)
        if h == hash_to_check:
            return count
    return 0


def pwned_api_check(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    response = request_api_data(sha1password[:5])
    return get_password_leaks_count(response, sha1password[5:])


def main(password):
    count = pwned_api_check(password)
    if count:
        Write.Print(f'{password} was found {count} times... You should probably change your password.', Colors.purple_to_red, interval=000.05)
    else:
        Write.Print(f'{password} was NOT found. Carry on!', Colors.purple_to_blue, interval=000.05)
    return 'All passwords checked!'


main(Write.Input("Enter your password > ", Colors.red_to_green, interval=000.10))
