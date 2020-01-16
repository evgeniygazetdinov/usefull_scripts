from django.db.models import F, Func, Value
from apps.news.models import News
News.objects.filter(long_description__icontains = '<center>').update(long_description=Func(F('long_description'),Value('<center>'),Value('<div style="text-align: center">'),function='replace'))
News.objects.filter(long_description__icontains = '</center>').update(long_description=Func(F('long_description'),Value('</center>'),Value('</div'>),function='replace')) 
News.objects.filter(long_description__icontains = '<br>').update(long_description=Func(F('long_description'),Value('<br>'),Value('p'),function='replace'))   
