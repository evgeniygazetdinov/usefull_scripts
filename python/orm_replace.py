from django.db.models import F, Func, Value
from myapp.models import News
News.objects.filter(long_description__icontains = '<br>').update(long_description=Func(F('long_description'),Value('<br>'),Value('p'),function='replace'))
