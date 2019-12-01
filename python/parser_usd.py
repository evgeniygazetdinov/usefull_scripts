from bs4 import BeautifulSoup
import requests
import json


def course():
    page = requests.get("https://www.fxempire.com/markets/usd-rub/overview")
    soup = BeautifulSoup(page.content,'html.parser')
    actual = (soup.find_all("div",class_ = 'DirectionBackgroundColor__BackgroundColor-sc-1qjm64q-0 fgRxHG'))
    changes = (soup.find_all("span",class_ = "Span-sc-1abytr7-0 bJRcAQ"))
    actual_course = actual[0].get_text()
    changes = changes[0].get_text()
    return actual_course,changes

def to_json(course,changes):
    rates = json.dumps({'base':'USD','target':'RUB','price':course,'changes':changes})
    return rates


if __name__ == "__main__":
    rub,changes = course()
    rates = to_json(rub,changes)
    print(rates)
