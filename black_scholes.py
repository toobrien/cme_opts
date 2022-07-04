from math       import exp, log, sqrt
from numpy      import arange
from statistics import NormalDist


N = NormalDist().cdf


def price(
    call:   bool,
    und:    float,
    strike: float,
    time:   float,
    vol:    float,
    rate:   float
) -> float:

    d1_ =   1 / (vol * sqrt(time)) * \
            (log(und / strike) + (rate + vol**2 / 2) * time)
    
    d2_ =   d1_ - vol * sqrt(time)

    disc =  exp(-rate * time) * strike

    if call:
        
        return N(d1_) * und - N(d2_) * disc

    else:

        return N(-d2_) * disc - N(-d1_) * und


def search(
    base:   float, 
    start:  float,
    stop:   float,
    step:   float,
    call:   bool,
    und:    float,
    strike: float,
    time:   float,
    prem:   float,
    rate:   float
):

    vol = base

    for i in arange(start, stop, step):

        vol  = base + i
        cost = price(call, und, strike, time, vol, rate)

        if cost > prem:

            break

    return vol - step


def iv(
    call:   bool,
    und:    float,
    strike: float,
    time:   float,
    prem:   float,
    rate:   float
) -> float:

    # searches down to tenth of percentage

    vol = 0.0001
    vol = search(vol, 0, 10, 0.1, call, und, strike, time, prem, rate)      # 10%
    vol = search(vol, 0, 0.1, 0.01, call, und, strike, time, prem, rate)    # 1%
    vol = search(vol, 0, 0.01, 0.001, call, und, strike, time, prem, rate)  # 0.1%

    return vol