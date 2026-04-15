import time, hmac, hashlib, base64, requests
from state import state

BASE = "https://api.bitget.com"

def sign(ts, method, path, body=""):
    msg = str(ts)+method+path+body
    return base64.b64encode(
        hmac.new(state["api_secret"].encode(), msg.encode(), hashlib.sha256).digest()
    ).decode()

def headers(method,path,body=""):
    ts = str(int(time.time()*1000))
    return {
        "ACCESS-KEY": state["api_key"],
        "ACCESS-SIGN": sign(ts,method,path,body),
        "ACCESS-TIMESTAMP": ts,
        "ACCESS-PASSPHRASE": state["passphrase"],
        "Content-Type":"application/json"
    }

def place_order(side, price, size):
    if state["mode"] != "live":
        print("PAPER ORDER", side, price, size)
        return

    path="/api/mix/v1/order/placeOrder"
    body={
        "symbol":state["symbol"],
        "marginCoin":"USDT",
        "size":str(size),
        "price":str(price),
        "side":side.lower(),
        "orderType":"limit"
    }

    requests.post(BASE+path,headers=headers("POST",path,str(body)),json=body)

def place_oco(side,tp,sl,size):
    if state["mode"] != "live":
        print("PAPER OCO",tp,sl)
        return

    path="/api/mix/v1/order/placeTPSL"
    body={
        "symbol":state["symbol"],
        "marginCoin":"USDT",
        "planType":"profit_loss",
        "triggerPrice":str(tp),
        "stopLossTriggerPrice":str(sl),
        "holdSide": "long" if side=="BUY" else "short"
    }

    requests.post(BASE+path,headers=headers("POST",path,str(body)),json=body)
