#! /usr/bin/env python
# -*- coding: utf-8 -*-
#change to russian
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pytube import YouTube
def find_links():
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    driver=webdriver.Chrome(chrome_options=options,)
    driver.get("https://www.youtube.com/")
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input#search"))).send_keys("algoritms by python")
    driver.find_element_by_css_selector("button.style-scope.ytd-searchbox#search-icon-legacy").click()
    print([my_href.get_attribute("href") for my_href in WebDriverWait(driver, 5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "a.yt-simple-endpoint.style-scope.ytd-video-renderer#video-title")))])


def download(link):
    path = os.getcwd()+'/downloaded_videos'
    yt = YouTube(link)
    yt = yt.get('mp4', '720p')
    yt.download(path)
    if not os.path.exists(path):
        os.makedirs(path)

def main():
    links = find_links()
    map(download,links)
    for i in links:
        print(str(i)+ ' will be downloaded')
