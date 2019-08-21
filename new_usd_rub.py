import json
from  forex_python.converter import CurrencyRates
from datetime import datetime, timedelta

def find_price_day_ago(USD,RUB):
    date_one_days_ago = datetime.now() - timedelta(days = 1)
    cour = CurrencyRates()
    price_day_ago = cour.convert(USD,RUB,1,date_one_days_ago)
    return price_day_ago

def calculate_diff(actual,price_day_ago):
    diff = actual - price_day_ago
    if diff < 0:
        diff = price_day_ago - actual
        return '-{}'.format(diff)
    else:
        return '+ {}'.format(diff)

def get_current_rates(USD,RUB):
    now = datetime.now()
    cour = CurrencyRates()
    actual = cour.convert(USD,RUB,1,now)
    price_day_ago = find_price_day_ago(USD,RUB)
    daily_changes = calculate_diff(actual,price_day_ago)
    rates = json.dumps({'base':USD,'target':RUB,'price':actual,'changes':daily_changes})
    return rates


if __name__ == '__main__':
    get_current_rates('USD','RUB')
