import asyncio


async def hello():
    print("Hello ...")
    await asyncio.sleep(2)  # time
    return "... World!"


async def main():
    result = await asyncio.gather(hello(), hello())  # immediately starts, result is list in order of starting
    print(result)


asyncio.run(main())
