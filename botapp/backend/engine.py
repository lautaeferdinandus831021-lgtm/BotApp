import pandas as pd, asyncio
from state import state

def macd(s,f,sl):
    return s.ewm(span=f).mean()-s.ewm(span=sl).mean()

async def engine_loop():
    while True:
        try:
            if len(state["candles_m1"])<30:
                await asyncio.sleep(1)
                continue

            close=pd.Series([c["close"] for c in state["candles_m1"]])

            state["macd"]={
                "fast": macd(close,2,3).iloc[-2:].tolist(),
                "mid": macd(close,3,4).iloc[-2:].tolist(),
                "slow": macd(close,4,5).iloc[-2:].tolist()
            }

            # 🔥 PNL
            if state["position"]:
                price=state["price"]
                entry=state["entry"]

                pnl = (price-entry) if state["position"]=="long" else (entry-price)
                state["pnl"] = round(pnl*state["size"],4)

        except:
            pass

        await asyncio.sleep(0.2)
