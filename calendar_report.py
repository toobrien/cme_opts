from black_scholes  import iv
from chain_set      import chain_set
from datetime       import datetime
from enum           import IntEnum
from structs        import opt_row
from sys            import argv
from time           import time
from util           import get_chain_set


START       = "1900-01-01"
END         = "2100-01-01"
DATE_FMT    = "%Y-%m-%d"
RATE        = 0.03
DPY         = 252


def get_width(front_date, back_date):

    return (datetime.strptime(back_date, DATE_FMT) - datetime.strptime(front_date, DATE_FMT)).days


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


# instantiate with get_calendar()

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
        self.width  = get_width(front_exp, back_exp)
        self.rows   = []

    
    def get_type(self):             return self.type 
    def get_front_exp(self):        return self.front_exp
    def get_front_ul(self):         return self.front_ul
    def get_front_class(self):      return self.front_class
    def get_back_exp(self):         return self.back_exp
    def get_back_ul(self):          return self.back_ul
    def get_back_class(self):       return self.back_class
    def get_strike_or_delta(self):  return self.strike_or_delta
    def get_id(self):               return self.id
    def get_width(self):            return self.width
    def get_rows(self):             return self.rows


def get_calendar(
    cs:                 chain_set,
    type:               int,
    front_leg_expiry:   str,
    back_leg_expiry:    str,
    strike:             float,
    delta:              float
):

    cal   = None
    dates = cs.get_dates()

    for date in dates:

        expiries = cs.get_expiries_by_date(date)

        if front_leg_expiry in expiries and back_leg_expiry in expiries:

            front_cd    = cs.get_chain_day(date, front_leg_expiry)
            back_cd     = cs.get_chain_day(date, back_leg_expiry)

            front_opt   = None
            back_opt    = None

            if strike:
            
                front_opt   = front_cd.get_opt_by_strike(type, strike)
                back_opt    = back_cd.get_opt_by_strike(type, strike)

            elif delta:

                front_opt       = front_cd.get_opt_by_delta(type, delta)
                front_strike    = front_opt[opt_row.strike]
                back_opt        = back_cd.get_opt_by_strike(type, front_strike)

            if not front_opt or not back_opt:

                continue

            if not cal:

                cal = calendar(
                        type,
                        front_leg_expiry,
                        front_opt[opt_row.underlying_id], 
                        front_opt[opt_row.symbol],
                        back_leg_expiry,
                        back_opt[opt_row.underlying_id],
                        back_opt[opt_row.symbol],
                        strike if strike else delta
                    )

            rows = cal.get_rows()

            # redefine in case delta was passed, rather than strike

            front_strike    = front_opt[opt_row.strike]

            front_exp       = front_opt[opt_row.expiry]
            front_delta     = front_opt[opt_row.settle_delta]
            front_dte       = max(0, get_width(date, front_exp))
            front_settle    = front_opt[opt_row.settle]
            front_ul_settle = front_cd.get_underlying_settle()
            front_iv        = iv(
                                type, 
                                front_ul_settle, 
                                front_strike,
                                front_dte / 252,
                                front_settle,
                                RATE
                            )

            back_exp        = back_opt[opt_row.expiry]
            back_delta      = back_opt[opt_row.settle_delta]
            back_dte        = max(0, get_width(date, back_exp))
            back_settle     = back_opt[opt_row.settle]
            back_ul_settle  = back_cd.get_underlying_settle()
            back_iv         = iv(
                                type,
                                back_ul_settle,
                                front_strike,
                                back_dte / 252,
                                back_settle,
                                RATE
                            )

            rows.append(
                (
                    date,
                    front_settle,
                    front_dte,
                    front_iv,
                    front_delta,
                    front_ul_settle,
                    back_settle,
                    back_dte,
                    back_iv,
                    back_delta,
                    back_ul_settle
                )
            )

    return cal


def report(
    cs:                 chain_set,
    ref_type:           int,
    ref_strike:         float,
    ref_front_leg_exp:  str,
    ref_back_leg_exp:   str,
    width_margin:       int
):

    # set reference delta from latest settlement of user-specified front leg
    # front leg delta is the basis for comparing spreads

    calendars   = {}
    ref_cal     = None
    ref_delta   = None
    ref_width   = get_width(ref_front_leg_exp, ref_back_leg_exp)
    dates       = cs.get_dates()

    # get delta for front leg of user-specified calendar

    for date in reversed(dates):

        expiries = cs.get_expiries_by_date(date)

        if ref_front_leg_exp in expiries and ref_back_leg_exp in expiries:

            cd = cs.get_chain_day(date, front_leg_expiry)

            opt = cd.get_opt_by_strike(ref_type, ref_strike)

            if opt:

                ref_delta = opt[opt_row.settle_delta]

            if ref_delta:

                break

    if not ref_delta:

        print("reference calendar not found. please check inputs.")

        return

    # build reference (user-specified) calendar

    id = (ref_front_leg_exp, ref_back_leg_exp, ref_strike, ref_type)

    ref_cal = get_calendar(cs, ref_type, ref_front_leg_exp, ref_back_leg_exp, ref_strike, None)

    calendars[id] = ref_cal

    # build calendars

    for date in dates:

        for i in range(len(expiries) - 1):

            front_exp = expiries[i]

            for j in range(i + 1, len(expiries)):

                back_exp = expiries[j]

                width = get_width(front_exp, back_exp)

                if ref_width - width_margin <= width <= ref_width + width_margin:

                    id = (front_exp, back_exp, ref_delta, ref_type)

                    if id not in calendars and not (front_exp == front_leg_expiry and back_exp == back_leg_expiry):
                    
                        calendars[id] = get_calendar(cs, ref_type, front_exp, back_exp, None, ref_delta)


if __name__ == "__main__":

    symbol              = argv[1]
    type                = argv[2]
    strike              = float(argv[3])
    defs                = argv[4].split(":")
    front_leg_expiry    = defs[0]
    back_leg_expiry     = defs[1]
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
        front_leg_expiry,
        back_leg_expiry,
        width_margin
    )

    print(f"elapsed: {time() - t0: 0.1f}")