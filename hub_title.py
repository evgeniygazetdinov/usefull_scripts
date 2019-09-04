from bs4 import BeautifulSoup
import requests
import json
import random


def find_titles():
    page = requests.get("https://rt.pornhub.com/")
    soup = BeautifulSoup(page.content,'html.parser')
    actual = (soup.find_all("span",class_ = 'title'))
    titles = []
    for i in range(len(actual)):
        titles.append(actual[i].get_text())
    return titles

def to_json(titles):
    secure_random = random.SystemRandom()
    rates = json.dumps({'random_title':secure_random.choices(titles)})
    return rates


if __name__ == "__main__":
 #   rates = to_json(rub,changes)
  #  print(rates)
    titles = find_titles()
    random_json = to_json(titles)
    print(random_json)
