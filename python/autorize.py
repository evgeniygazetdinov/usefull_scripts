import time


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

browser = webdriver.Chrome()
browser.get('https://spb.hh.ru/search/vacancy?text=&area=2')
search = browser.find_element_by_name('password')
search.send_keys("")
search.send_keys(Keys.RETURN)

