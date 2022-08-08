from chain_set  import chain_set
from datetime   import date
from enum       import IntEnum
from structs    import opt_row
from sys        import argv
from time       import time
from typing     import List
from util       import get_chain_set


START       = "1900-01-01"
END         = "2100-01-01"
DATE_FMT    = "%Y-%m-%d"


class calendar_row(IntEnum):

    date            = 0
    front_settle    = 1
    front_dte       = 2
    front_iv        = 3
    front_delta     = 4
    front_ul_settle = 5
    back_settle     = 6
    back_dte        = 7
    back_iv         = 8
    back_delta      = 9
    back_ul_settle  = 10


class calendar():


    def __init__(
        self,
        type:               int,
        front_exp:          str,
        front_ul:           str,
        front_class:        str,
        back_exp:           str,
        back_ul:            str,
        back_class:         str,
        strike_or_delta:    float
    ):

        self.type               = type
        self.front_exp          = front_exp
        self.front_ul           = front_ul
        self.front_class        = front_class
        self.back_exp           = back_exp
        self.back_ul            = back_ul
        self.back_class         = back_class
        self.strike_or_delta    = strike_or_delta

        self.id     = (front_exp, back_exp, strike_or_delta, type)
        self.width  = (date.strptime(back_exp, DATE_FMT) - date.strptime(front_exp, DATE_FMT)).days
        self.rows   = None


def report(
    cs:                 chain_set,
    type:               int,
    strike:             float,
    front_leg_symbol:   str,
    front_leg_expiry:   str,
    back_leg_symbol:    str,
    back_leg_expiry:    str,
    width_margin:       int
):

    # set reference delta from latest settlement of user-specified front leg
    # front leg delta is the basis for comparing spreads

    ref_delta   = None
    dates       = cs.get_dates()
    i           = len(dates) - 1

    while i >= 0:

        cur_date = dates[i]

        expiries = cs.get_expiries_by_date(cur_date)

        for expiry in expiries:

            cd = cs.get_chain_day(cur_date, expiry)

            if cd.symbol == front_leg_symbol and cd.expiry == front_leg_expiry:

                opt = cd.get_opt_by_strike(type, strike)

                if (opt):

                    ref_delta = opt[opt_row.settle_delta]
                
                    break

                else:

                    # no such strike, can't create report

                    return

    if not ref_delta:

        # front leg not found

        return

    # build user-specified spread (by strike)

    
    
    # build historical spreads (by delta)


    pass


if __name__ == "__main__":

    symbol              = argv[1]
    type                = argv[2]
    strike              = float(argv[3])
    defs                = argv[4].split(",")
    front_leg           = defs[0].split(":")
    back_leg            = defs[1].split(":")
    width_margin        = int(argv[5])
    excluded_classes    = []

    if len(argv) > 5:

        excluded_classes = argv[6:]

    t0 = time()

    cs = get_chain_set(symbol, START, END, excluded_classes)

    report(
        cs,
        1 if type == "call" else 0,
        strike,
        front_leg[0],
        front_leg[1],
        back_leg[0],
        back_leg[1],
        width_margin
    )

    print(f"elapsed: {time() - t0: 0.1f}")