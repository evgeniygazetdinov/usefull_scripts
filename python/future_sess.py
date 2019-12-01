from django import template
from requests_futures.sessions import FuturesSession
import time



register = template.Library()
@register.filter
def parse_url(urls):
    start_time = time.clock()
    res = []
    locations = []
    for i in urls:
        if i['location']:
            locations.append(str(i['location']))
    session = FuturesSession()        
    for i in range(len(locations)):
        if i%2== 0:
            print(i)
            s1 = session.get(locations[i])
            first_response = s1.result()
            if first_response.status_code == 200:
                print('200',locations[i])
                res.append([200,locations[i]])
        else :
            print(i)
            s2 = session.get(locations[i])
            second_response = s2.result()
            if second_response.status_code == 200:
                print('200',locations[i])
                res.append([200,locations[i]])
    print(len(res))
    print(time.clock() - start_time, "seconds")
    return res
