import pytz
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin
import os
import requests



class Timezonemiddleware(MiddlewareMixin):
    def process_request(self,request):
        #obtain_timezone from ip
        response_with_time_zone = requests.get('http://worldtimeapi.org/api/ip/')
        timezone_json = response_with_time_zone.json()
        user_time_zone = timezone_json['timezone']
        if user_time_zone:
            request.session['user_time_zone'] = user_time_zone
        return None




