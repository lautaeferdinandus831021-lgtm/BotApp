import websockets,json,time
from state import state

m1=None
m5=None

def update_m1(p):
    global m1
    t=int(time.time()//60)

    if not m1 or m1["time"]!=t:
        if m1:
            state["candles_m1"].append(m1)
            state["candles_m1"]=state["candles_m1"][-500:]
        m1={"time":t,"open":p,"high":p,"low":p,"close":p}
    else:
        m1["high"]=max(m1["high"],p)
        m1["low"]=min(m1["low"],p)
        m1["close"]=p

def update_m5(p):
    global m5
    t=int(time.time()//300)

    if not m5 or m5["time"]!=t:
        state["candle_m5"]=m5
        m5={"time":t,"open":p,"high":p,"low":p,"close":p}
    else:
        m5["high"]=max(m5["high"],p)
        m5["low"]=min(m5["low"],p)
        m5["close"]=p

def update_delta(t):
    if t.get("side")=="buy":
        state["delta"]+=float(t["size"])
    else:
        state["delta"]-=float(t["size"])

async def run_ws_public():
    url="wss://ws.bitget.com/v2/ws/public"

    async with websockets.connect(url) as ws:
        await ws.send(json.dumps({
            "op":"subscribe",
            "args":[
                {"channel":"trade","instId":"BTCUSDT"},
                {"channel":"books","instId":"BTCUSDT"}
            ]
        }))

        async for msg in ws:
            d=json.loads(msg)
            if "data" not in d: continue

            data=d["data"]

            if "price" in data[0]:
                for t in data:
                    p=float(t["price"])
                    state["price"]=p
                    update_m1(p)
                    update_m5(p)
                    update_delta(t)

            if "bids" in data[0]:
                ob=data[0]
                state["orderbook"]={
                    "bids":ob.get("bids",[])[:5],
                    "asks":ob.get("asks",[])[:5]
                }
