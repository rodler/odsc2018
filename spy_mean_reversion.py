import numpy as np
from collections import deque
import datetime

def initialize(context):
    set_commission(commission.PerTrade(cost=0.0))
    set_slippage(slippage.VolumeShareSlippage(volume_limit=0.25, price_impact=0.0))
    context.stock = symbol('SPY')
    context.inpos = 0
    context.pnls = 0


def handle_data(context, data):
    s1 = context.stock

    price = data.current(s1,'price')
    sma = np.mean(data.history(s1,'price',10000,frequency='1m'))
    if (price - sma) > 6 and context.inpos==0:
        order_target_percent(s1,-1)
        context.inpos = -1
        print('Enter Short',price-sma,price)
        context.entry = price

    elif (price - sma) < 0 and context.inpos==-1:
        order_target_percent(s1,0)
        context.inpos = 0
        context.pnls += context.entry - price
        print('Exit Short',price-sma,price,context.pnls)

    elif (price - sma) < -6 and context.inpos==0:
        order_target_percent(s1,1)
        context.inpos = 1
        context.entry = price
        print('Enter Long',price-sma,price)

    elif (price - sma) > 0 and context.inpos==1:
        order_target_percent(s1,0)
        context.inpos = 0
        context.pnls += price - context.entry
        print('Exit Long',price-sma,price,context.pnls)

    record('resid',price-sma)
