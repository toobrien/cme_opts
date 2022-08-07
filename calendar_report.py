from chain_set  import chain_set
from datetime   import date
from enum       import IntEnum
from sys        import argv
from time       import time
from typing     import List
from util       import get_chain_set


START       = "1900-01-01"
END         = "2020-01-01"
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
        front_exp:      str,
        front_ul:       str,
        front_class:    str,
        back_exp:       str,
        back_ul:        str,
        back_class:     str,
        strike:         float
    ):

        self.front_exp      = front_exp
        self.front_ul       = front_ul
        self.front_class    = front_class
        self.back_exp       = back_exp
        self.back_ul        = back_ul
        self.back_class     = back_class
        self.strike         = strike

        self.id     = (front_exp, back_exp, strike)
        self.width  = (date.strptime(back_exp, DATE_FMT) - date.strptime(front_exp, DATE_FMT)).days
        self.rows   = None


def report(
    cs:             chain_set,
    strike:         float,
    width_range:    List[int]
):

    pass


if __name__ == "__main__":

    symbol      = argv[1]
    strike      = float(argv[2])
    width_range = [ int(x) for x in argv[3].split(":") ]

    t0 = time()

    cs = get_chain_set(symbol, START, END, [])

    report(cs, strike, width_range)

    print(f"elapsed: {time() - t0: 0.1f}")

    pass