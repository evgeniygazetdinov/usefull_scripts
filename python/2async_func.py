import asyncio
from time import time

start = time()
async def get_messages(some):
    i = 0
    while True:
        print(i)
        i+=1
        await asyncio.sleep(0.1)

async def check_user(some):
    await asyncio.sleep(10)
    print('user do nothing')


task = [ asyncio.ensure_future(get_messages('some')),
asyncio.ensure_future(check_user('some'))
]
event_loop = asyncio.get_event_loop()
event_loop.run_until_complete(asyncio.gather(*task))
print('{:.2F}'.format(time()-start))
