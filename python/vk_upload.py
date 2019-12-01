from urllib.request import urlretrieve
import vk, os, time, math
from passport import vk_id, login password


session = vk.AuthSession(app_id=vk_id, user_login=login, user_password=password)

vkapi = vk.API(session)
print(vkapi)
