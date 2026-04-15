import asyncio, random, time
from state import state
from execution import execute

async def loop():
    while True:
        if state["price"] == 0:
            state["price"] = 100

        state["price"] += random.uniform(-1,1)

        candle={
            "time":int(time.time()),
            "open":state["price"]-1,
            "high":state["price"]+1,
            "low":state["price"]-2,
            "close":state["price"]
        }

        state["candles_m1"].append(candle)
        state["candles_m1"]=state["candles_m1"][-200:]

        execute()

        await asyncio.sleep(1)
