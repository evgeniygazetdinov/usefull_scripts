import asyncio
from time import time

start = time()
def second_check():
    print('xa')


async def get_messages():
    i = 0
    while i<20:
        print(i)
        i+=1
        await asyncio.sleep(1)


async def check_user():
    await asyncio.sleep(10)
    print('user do nothing')

def main():
    while True:
        task = [ asyncio.ensure_future(get_messages()),
        asyncio.ensure_future(check_user())
        ]
        event_loop = asyncio.get_event_loop()
        event_loop.call_later(8,second_check)
        event_loop.run_until_complete(asyncio.gather(*task))
        print('{:.2F}'.format(time()-start))
main()
