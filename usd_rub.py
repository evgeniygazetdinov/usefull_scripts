import json
from  forex_python.converter import CurrencyRates
import datetime

def get_current_rates(USD,RUB):
    now = datetime.datetime.now()
    cour = CurrencyRates()
    actual = cour.convert(USD,RUB,1,now)
    rates = json.dumps({'base':USD,'target':RUB,'price':actual,'date':now.isoformat()})
    return rates


if __name__ == '__main__':

    print(get_current_rates('USD','RUB'))
