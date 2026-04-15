import asyncio,uvloop
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

from ws_public import run_ws_public
from engine import engine_loop
from execution import execute_trade

async def loop():
    while True:
        try:
            execute_trade()
        except Exception as e:
            print("ERR",e)
        await asyncio.sleep(0.2)

async def main():
    await asyncio.gather(
        run_ws_public(),
        engine_loop(),
        loop()
    )

asyncio.run(main())
