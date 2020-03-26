#!/usr/bin/env python3

import asyncio
import time
import sys


now = time.time()

async def check_port(ip, port, loop):	
    conn = asyncio.open_connection(ip, port, loop=loop)
	
    try:
        reader, writer = await asyncio.wait_for(conn, timeout=3)
        print('Scanning...')
        print('IP Address:', ip)
        print('Port:', port)
        return(ip, port, True)
    
    except:
        print('Failed to scan')
        print('IP Address:', ip)
        print('Port:', port)
        return(ip, port, False)

async def run(dests, ports, loop):
    tasks = [asyncio.ensure_future(check_port(d, p, loop)) for d in dests for p in ports]
    responses = await asyncio.gather(*tasks)
    return responses

ports = list(map(float, str(sys.argv[2]).strip('[]').split(',')))
dests = []

for i in range(1, 255):
    ip_address = str(sys.argv[1]) + '.' +str(i)
    dests.append(ip_address)

loop = asyncio.get_event_loop()
future = asyncio.ensure_future(run(dests, ports, loop))
loop.run_until_complete(future)
print('#'*50)
print('Results: ', future.result())
print('#'*50)
	
