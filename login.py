from secret import secret
from selenium import webdriver

url = "https://vk.com"


driver = webdriver.Chrome()
driver.get(url)

user_name = driver.find_element_by_id("index_email")
user_name.send_keys(secret['login'])
user_password = driver.find_element_by_id('index_pass')
user_password.send_keys(secret['password'])
driver.find_element_by_id('index_login_button').click()

print("Successful!")

