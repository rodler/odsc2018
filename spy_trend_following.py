import quantopian.algorithm as algo
import numpy as np


def initialize(context):

    context.stock = symbol('SPY')
    context.inpos = 0

    # Rebalance every day, 1 min before close.
    algo.schedule_function(
        rebalance,
        algo.date_rules.every_day(),
        algo.time_rules.market_close(minutes=3),
    )

def rebalance(context, data):
    """
    Execute orders according to our schedule_function() timing.
    """
    s1 = context.stock
    price = data.current(s1,'price')
    sma = np.mean(data.history(s1,'price',300,frequency='1d'))

    if (price - sma) < 0 and context.inpos>=0:
        order_target_percent(s1,-1)
        context.inpos = -1
        print('Enter Short',price-sma,price)
        context.entry = price

    elif (price - sma) > 0 and context.inpos<=0:
        order_target_percent(s1,1)
        context.inpos = 1
        context.entry = price
        print('Enter Long',price-sma,price)
