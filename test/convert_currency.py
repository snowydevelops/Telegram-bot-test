import requests

def exchange_rate(base, target):
    url = f'https://api.exchangerate-api.com/v4/latest/{base}'
    reponse = requests.get(url)
    if reponse.status_code !=200:
        return 'ERROR'
    else:
        reponse = reponse.json()
        return reponse['rates'][target]


if __name__ == '__main__':
    base = input('enter base currency: ').upper()
    target = input('enter base currency: ').upper()
    rate = exchange_rate(base, target)
    print(rate)