import requests

#from cachetools import cached, TTLCache

#cache = TTLCache(maxsize=100, ttl=3*60*60)


def get_currency_list(base_currency = 'USD'):

    url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return list(response.json()['rates'].keys())



#@cached(cache)
def get_exchange_rate(base_currency, target_currency):
    url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.json()['rates'][target_currency]

#@cached(cache)
def get_exchange_rate_single(base_currency):
    url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.json()['rates']

def convert_currency(amount, exchange_rate):
    return amount * exchange_rate


if __name__ == '__main__':
    base_currency = input("Enter base currency: ").upper()
    target_currency = input("Enter target currency: ").upper()
    exchange_rate = get_exchange_rate(base_currency, target_currency)
    print(f'rate of {base_currency} to {target_currency} is {exchange_rate}')
    # amount = float(input("Enter amount: "))
    # # print(get_currency_list())
    # exchange_rate = get_exchange_rate(base_currency, target_currency)
    # converted_amount = convert_currency(amount, exchange_rate)
    # print(f"{amount} {base_currency} is {converted_amount} {target_currency}")