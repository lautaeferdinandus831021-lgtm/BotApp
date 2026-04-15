from bitget_api import get_balance
from config import *
from state import state

def can_trade():
    bal=get_balance()
    print("💰",bal)

    if bal < MIN_BALANCE:
        print("⚠️ ANALISA ONLY")
        return False
    return True

def calc_size(price):
    bal=get_balance()
    return round((bal*MAX_RISK)/price,4)

def calc_tpsl_m5(side):
    c=state.get("candle_m5")
    if not c: return None,None

    if side=="BUY":
        return c["high"],c["low"]
    else:
        return c["low"],c["high"]
