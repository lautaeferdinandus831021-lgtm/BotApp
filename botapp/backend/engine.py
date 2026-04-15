import asyncio, random, time
from state import state
from bitget import get_balance

def gen_candle(prev):
    o = prev["close"]
    c = o + random.uniform(-1,1)
    h = max(o,c) + random.uniform(0,1)
    l = min(o,c) - random.uniform(0,1)
    return {"time": int(time.time()), "open": o, "high": h, "low": l, "close": c}

async def loop():
    state["candles_m1"] = [{
        "time": int(time.time()),
        "open":100,"high":101,"low":99,"close":100
    }]

    while True:
        # ================= SIMULASI PRICE =================
        last = state["candles_m1"][-1]
        new = gen_candle(last)
        state["candles_m1"].append(new)

        state["price"] = new["close"]
        state["pnl"] = random.uniform(-5,5)

        # ================= REAL BALANCE (BITGET) =================
        try:
            if state.get("api_key"):
                bal = get_balance(state)
                state["balance"] = bal
        except Exception as e:
            state["balance"] = {"error": str(e)}

        await asyncio.sleep(1)
