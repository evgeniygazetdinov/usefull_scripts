from __future__ import division
import pytz
from datetime import datetime, timedelta
from django.db import models
from django.utils import timezone
from pytz.exceptions import UnknownTimeZoneError






def time_kanal_match(dt):
   
    if not dt:
        return False, 0

    hours = (0, 2, 3, 7)
    if timezone.now() > dt.replace(tzinfo=None):
        diff_hour = timezone.now() - dt.replace(tzinfo=None)
    else:
        diff_hour = dt.replace(tzinfo=None) - timezone.now()

    return abs(int(round(diff_hour.seconds / 3600))) in hours, int(round(diff_hour.seconds / 3600))


class TVProgrammItemManager(models.Manager):
   
    def big_animation(self, tz=None):
        """
        Блок с большой анимацией на главной
        :return: отсортированный qs
        """
        qs = self.filter(
            date_start__gte=timezone.now(),
            date_start__hour=19,
            date_start__minute=30,
            program__not_show=False
        ).order_by('date_start')

        if len(qs) == 0:
            return qs

        if not tz:
            return qs

        local_time = get_local_time(tz)
        match, hours = time_kanal_match(local_time)

        if match:
            for item in qs:
                item.date_start += timedelta(hours=hours)
        else:
            qs = qs.filter(
                date_start__gte=local_time,
                date_start__hour=19,
                date_start__minute=30,
                program__not_show=False
            ).order_by('date_start')

        return qs
