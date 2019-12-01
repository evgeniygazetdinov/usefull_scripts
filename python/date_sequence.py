import datetime


#generate with diff



dt  = datetime.datetime(1991,03,20)
end = datetime.datetime(1991,03,20,23,59,59)
step = datetime.timedelta(hours = 5)
results = []
while dt<end:
    results.append(dt.strftime('%Y-%m-%d %H:%M:%S'))
    dt += step

print(results)
