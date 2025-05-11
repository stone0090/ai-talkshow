import os

import pyvts
import asyncio
import random
from datetime import datetime, timedelta

from pyvts import vts_request


async def authentication_token(vts_port):
    print(f'vts_authenticate for {vts_port}')
    token_path = f'tmp/vts_token_{vts_port}.txt'
    myvts = pyvts.vts(port=vts_port, token_path=token_path)
    myvts.vts_request = vts_request.VTSRequest(
        developer=f'stone',
        plugin_name=f'pyvts_{vts_port}'
    )
    result = myvts.vts_request.authentication_token()
    print(result)


async def vts_authenticate(vts_port):
    print(f'vts_authenticate for {vts_port}')
    token_path = f'tmp/vts_token_{vts_port}.txt'
    myvts = pyvts.vts(port=vts_port, token_path=token_path)
    myvts.vts_request = vts_request.VTSRequest(
        developer=f'stone',
        plugin_name=f'pyvts_{vts_port}'
    )
    authentic_token = None
    try:
        authentic_token = await myvts.read_token()
    except Exception as e:
        print(e)
    if authentic_token is not None:
        return
    if not os.path.exists('tmp'):
        os.mkdir('tmp')
    if os.path.exists(token_path):
        os.remove(token_path)
    await myvts.connect()
    await myvts.request_authenticate_token()
    await myvts.write_token()
    await myvts.close()


async def vts_open_mouth(vts_port, duration):
    print(f'vts_open_mouth for {duration} ms')
    token_path = f'tmp/vts_token_{vts_port}.txt'
    myvts = pyvts.vts(port=vts_port, token_path=token_path)
    myvts.vts_request = vts_request.VTSRequest(
        developer=f'stone',
        plugin_name=f'pyvts_{vts_port}'
    )
    await myvts.connect()
    await myvts.read_token()
    await myvts.request_authenticate()
    start_time = datetime.now()
    interval = timedelta(milliseconds=100)
    duration = timedelta(milliseconds=duration)
    while datetime.now() - start_time < duration:
        # 0到1的随机数
        await myvts.request(myvts.vts_request.requestSetParameterValue("MouthOpen", random.random()))
        await asyncio.sleep(interval.total_seconds())
    await myvts.close()


async def main():
    # 启动异步任务
    # task1 = asyncio.create_task(vts_open_mouth(8001, 5000))
    # task1 = asyncio.create_task(vts_authenticate(8002))
    # await asyncio.gather(task1)
    task2 = asyncio.create_task(vts_open_mouth(8002, 5000))
    await asyncio.gather(task2)



if __name__ == "__main__":
    # asyncio.run(vts_authenticate(8001))
    # asyncio.run(vts_authenticate(8001))
    # asyncio.run(vts_open_mouth(8001, 5000))
    # asyncio.run(vts_open_mouth(8002, 5000))
    asyncio.run(main())
