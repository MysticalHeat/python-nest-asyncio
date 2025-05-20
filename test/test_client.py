#!/usr/bin/env python
# -*- coding:utf-8 -*-

import asyncio
from nest import NestMsClient


async def print_time():
    count = 0
    while True:
        print(f"{count} seconds passed")
        count += 1
        await asyncio.sleep(1)


async def send_long_time_message():
    HOST = "dev.cryptoaimedia.geryon.space"
    PORT = 3511
    client = NestMsClient(HOST, PORT)
    pattern = "TEST_PATTERN"
    _, res = await client.send(pattern, None)
    print(res)
    pattern = {"cmd": "TEST_PATTERN"}
    _, res = await client.send(pattern, None)
    print(res)
    pattern = {"cmd": "test_decorator"}
    _, res = await client.send(pattern, "this is ok")
    print(res)


async def main():
    task1 = asyncio.create_task(send_long_time_message())
    task2 = asyncio.create_task(print_time())

    await asyncio.gather(task1, task2)


if __name__ == "__main__":

    asyncio.run(main())
