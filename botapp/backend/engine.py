import pandas as pd,asyncio
from state import state

def macd(s,f,sl):
    return s.ewm(span=f).mean()-s.ewm(span=sl).mean()

async def engine_loop():
    while True:
        try:
            if len(state["candles_m1"])<30:
                await asyncio.sleep(1)
                continue

            c=pd.Series([x["close"] for x in state["candles_m1"]])

            state["macd"]={
                "fast":macd(c,2,3).iloc[-2:].tolist(),
                "mid":macd(c,3,4).iloc[-2:].tolist(),
                "slow":macd(c,4,5).iloc[-2:].tolist()
            }
        except:
            pass

        await asyncio.sleep(0.2)
