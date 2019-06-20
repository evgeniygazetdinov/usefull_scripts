import urllib.request
from bs4 import BeautifulSoup
import ssl
import requests


def open_page():

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    with urllib.request.urlopen('https://www.strd.ru/',context = ctx) as response:
        html = response.read()
    return html

def find_images(page):
    imge = []
    soup = BeautifulSoup(page)
    for img in soup.findAll('img'):
        imge.append(img.get('src'))
    return imge

def download_stuff(img_link):
    name =0
    domen ='https://www.strd.ru/'
    print('error here')
    ssl._create_default_https_context = ssl._create_unverified_context
    for link in img_link:
        url = domen+link
        r = requests.get(str(url))
        with open('/img_folder/'+str(name)+'.jpg', 'wb') as f:
            f.write(r.content)
        name +=1
        f.close()

def main_func():
    page = open_page()
    img_link = find_images(page)
    download_stuff(img_link)
    print("mission complete")

if __name__ == "__main__":
    main_func()
