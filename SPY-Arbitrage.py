import quantopian.algorithm as algo
import numpy as np


def initialize(context):
    """
    Called once at the start of the algorithm.
    """
    # Rebalance every day, 1 hour after market open.
    algo.schedule_function(
        rebalance,
        algo.date_rules.every_day(),
        algo.time_rules.market_close(hours=1),
    )

    context.aapl = symbol('AAPL')
    context.xom = symbol('XOM')
    context.bhp = symbol('BHP')
    context.spy = symbol('SPY')
    context.inpos = 0

def rebalance(context, data):
    X1 = context.aapl
    X2 = context.xom
    X3 = context.bhp
    Y = context.spy
    P1 = data.history(X1,'price',200,'1d')
    P2 = data.history(X2,'price',200,'1d')
    P3 = data.history(X3,'price',200,'1d')
    N = data.history(Y,'price',200,'1d')
    w = [0.92919341,  0.8350131 ,  0.02745906]
    theo = w[0]*P1 + w[1]*P2 + w[2]*P3 - N + 35
    sd_theo = np.std(theo)
    if theo[-1] > 5 and context.inpos==0:
        order_target_percent(X1,-w[0]/sum(w))
        order_target_percent(X2,-w[1]/sum(w))
        order_target_percent(X3,-w[2]/sum(w))
        order_target_percent(Y,1)
        context.inpos = -1
        print "Enter Short"
        print context.portfolio.positions

    elif theo[-1] < 0 and context.inpos==-1:
        order_target_percent(X1,0)
        order_target_percent(X2,0)
        order_target_percent(X3,0)
        order_target_percent(Y,0)
        context.inpos = 0
        print "Exit Short"
        print context.portfolio.positions

    elif theo[-1] < -5 and context.inpos==0:
        order_target_percent(X1,w[0]/sum(w))
        order_target_percent(X2,w[1]/sum(w))
        order_target_percent(X3,w[2]/sum(w))
        order_target_percent(Y,-1)
        context.inpos = 1
        print "Enter Long"


    elif theo[-1] > 0 and context.inpos==1:
        order_target_percent(X1,0)
        order_target_percent(X2,0)
        order_target_percent(X3,0)
        order_target_percent(Y,0)
        context.inpos = 0
        print "Exit Long"

    record('theo',theo[-1])
