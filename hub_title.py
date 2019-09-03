from bs4 import BeautifulSoup
import requests
import json


def find_titles():
    page = requests.get("https://rt.pornhub.com/")
    soup = BeautifulSoup(page.content,'html.parser')
    actual = (soup.find_all("span",class_ = 'title'))
    return actual

#def to_json(course,changes):
#    rates = json.dumps({'base':'USD','target':'RUB','price':course,'changes':changes})
#    return rates


if __name__ == "__main__":
 #   rates = to_json(rub,changes)
  #  print(rates)
    titles = find_titles()
    print(titles)
