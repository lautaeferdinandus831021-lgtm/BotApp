import time,hmac,hashlib,base64,requests,json
from config import *

def sign(ts,method,path,body=""):
    msg=f"{ts}{method}{path}{body}"
    return base64.b64encode(
        hmac.new(API_SECRET.encode(),msg.encode(),hashlib.sha256).digest()
    ).decode()

def headers(method,path,body=""):
    ts=str(int(time.time()*1000))
    return {
        "ACCESS-KEY":API_KEY,
        "ACCESS-SIGN":sign(ts,method,path,body),
        "ACCESS-TIMESTAMP":ts,
        "ACCESS-PASSPHRASE":PASSPHRASE,
        "Content-Type":"application/json"
    }

def get_balance():
    path="/api/mix/v1/account/accounts"
    r=requests.get(BASE_URL+path,headers=headers("GET",path))
    try:
        for a in r.json()["data"]:
            if a["marginCoin"]==MARGIN:
                return float(a["available"])
    except:
        pass
    return 0

def place_limit(side,price,size):
    body={
        "symbol":SYMBOL,
        "marginCoin":MARGIN,
        "size":str(size),
        "price":str(price),
        "side":"open_long" if side=="BUY" else "open_short",
        "orderType":"limit",
        "timeInForceValue":"post_only"
    }

    path="/api/mix/v1/order/placeOrder"

    return requests.post(BASE_URL+path,
        json=body,
        headers=headers("POST",path,json.dumps(body))
    ).json()

def close_position(side,size):
    body={
        "symbol":SYMBOL,
        "marginCoin":MARGIN,
        "size":str(size),
        "side":"close_long" if side=="SELL" else "close_short",
        "orderType":"market",
        "reduceOnly":True
    }

    path="/api/mix/v1/order/placeOrder"

    return requests.post(BASE_URL+path,
        json=body,
        headers=headers("POST",path,json.dumps(body))
    ).json()

def place_tpsl(side,tp,sl,size):
    path="/api/mix/v1/plan/placePlan"

    tp_body={
        "symbol":SYMBOL,
        "marginCoin":MARGIN,
        "size":str(size),
        "triggerPrice":str(tp),
        "side":"close_long" if side=="BUY" else "close_short",
        "orderType":"market",
        "planType":"profit_plan"
    }

    sl_body={
        "symbol":SYMBOL,
        "marginCoin":MARGIN,
        "size":str(size),
        "triggerPrice":str(sl),
        "side":"close_long" if side=="BUY" else "close_short",
        "orderType":"market",
        "planType":"loss_plan"
    }

    requests.post(BASE_URL+path,json=tp_body,
        headers=headers("POST",path,json.dumps(tp_body)))

    requests.post(BASE_URL+path,json=sl_body,
        headers=headers("POST",path,json.dumps(sl_body)))
