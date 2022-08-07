from chain_set  import chain_set
from sys        import argv
from time       import time
from typing     import List
from util       import get_chain_set


START   = "1900-01-01"
END     = "2020-01-01"


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
        self.strike     = strike

        self.id     = (front_exp, back_exp, strike)
        self.rows   = None


def calendar_report(
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

    calendar_report(cs, strike, width_range)

    print(f"elapsed: {time() - t0: 0.1f}")

    pass