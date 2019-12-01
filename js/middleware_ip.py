import requests
from ipware import get_client_ip



class TimezoneMiddleware(object):
    def process_request(self, request):
        ip, is_routable = get_client_ip(request)
        response_ip = requests.get('https://freegeoip.app/json/{}?callback'.format(ip))
        time_by_ip = response_ip.json()
        ip_user_zone =time_by_ip['time_zone']
        f1 = open('2.txt','a+')
        f1.write('\n')
        f1.write(ip)
        f1.write('\n')
        f1.write(ip_user_zone)

        f1.write('\n')
        f1.close()
        request.session['user_time_zone'] = str(ip_user_zone)
        return None

