from order_manager import *
from risk import *
from partial import partial_tp
from bitget_api import place_limit,place_tpsl
from state import state

def execute_trade():

    price=state["price"]

    if not spread_filter():
        return

    partial_tp()

    if not can_trade():
        return

    if not is_m5_open():
        return

    macd=triple_macd_signal()
    delta=delta_filter()
    imb=imbalance_zone()
    absb=absorption_detection()

    signals=[macd,delta,imb]

    if absb:
        signals.append(absb)

    if all(s==signals[0] for s in signals if s):

        side=signals[0]
        entry=adaptive_price(side)
        size=calc_size(entry)

        print("🔥 REAL ENTRY:",side,entry,size)

        place_limit(side,entry,size)

        tp,sl=calc_tpsl_m5(side)

        if tp and sl:
            print("🎯 TP/SL:",tp,sl)
            place_tpsl(side,tp,sl,size)
