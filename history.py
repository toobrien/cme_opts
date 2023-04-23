from sys            import argv
from black_scholes  import iv
from chain_def      import chain_def
from datetime       import datetime, timedelta
from json           import loads
from structs        import opt_row
from util           import get_chain_day, get_expiries_for_underlying_and_class


# usage: python history.py ZW ZW1 90


SCALE_CONFIG    = loads(open("./contract_scale.json", "r").read())
FMT             = "%Y-%m-%d"
RATE            = 0.02


def validate_field(opts, row, col): 
                
    try: 

        return opts[row][col] 
                    
    except TypeError: 
    
        return -1.0


def get_row_text(opts: dict, idx: int, type: str, t: int):

    strike = validate_field(opts[type], idx, opt_row.strike)
    settle = validate_field(opts[type], idx, opt_row.settle)
    vol    = -1.0

    if strike != -1.0 and settle != -1.0:

        vol = iv(True, opts["ul_settle"], float(strike), t, float(settle), RATE)

    return strike, settle, vol


def report(
    ul: str,
    opt_class: str,
    days: int
):

    first_day   = datetime.today()
    exps        = []

    while True:
    
        exps = get_expiries_for_underlying_and_class(ul, opt_class, first_day.strftime(FMT))
        
        if exps:

            break

        first_day = first_day - timedelta(days = 1)

    #print(exps)
    #print(first_day.strftime("%Y-%m-%d"))

    for exp in exps:

        rows = []

        next_day    = first_day
        c_def       = chain_def(opt_class, ul, exp)
        i           = days

        while i > 0:

            day_str = next_day.strftime(FMT)
            c_day   = get_chain_day(c_def, day_str)

            if c_day:

                # rescale underlying for pricing

                if c_day.symbol in SCALE_CONFIG:

                    c_day.underlying_settle *= SCALE_CONFIG[c_day.symbol]

                c_50 = c_day.get_opt_by_delta(True, 0.50)
                c_15 = c_day.get_opt_by_delta(True, 0.15)
                c_05 = c_day.get_opt_by_delta(True, 0.05)

                p_50  = c_day.get_opt_by_delta(False, -0.50)
                p_15  = c_day.get_opt_by_delta(False, -0.15)
                p_05  = c_day.get_opt_by_delta(False, -0.05)

                rows.append(
                    {
                        day_str: {
                            "calls":    [ c_50, c_15, c_05 ], 
                            "puts":     [ p_50, p_15, p_05 ],
                            "ul_settle":  c_day.underlying_settle
                        }
                    }
                )

                i -= 1
            
            next_day = next_day - timedelta(days = 1)

        print(f"{ul:20}{opt_class:10}{exp:10}\n\n")

        print(
            f"date".rjust(12),
            f"c_50_str".rjust(10),
            f"c_50_stl".rjust(10),
            f"c_50_iv".rjust(10),
            f"c_15_str".rjust(10),
            f"c_15_stl".rjust(10),
            f"c_15_iv".rjust(10),
            f"c_05_str".rjust(10),
            f"c_05_stl".rjust(10),
            f"c_05_iv".rjust(10),
            f"p_50_str".rjust(10),
            f"p_50_stl".rjust(10),
            f"p_50_iv".rjust(10),
            f"p_15_str".rjust(10),
            f"p_15_stl".rjust(10),
            f"p_15_iv".rjust(10),
            f"p_05_str".rjust(10),
            f"p_05_stl".rjust(10),
            f"p_05_iv".rjust(10),
            "\n\n"
        )

        exp_dt = datetime.strptime(exp, FMT)

        for row in rows:

            for day, opts in row.items():

                t = (exp_dt - datetime.strptime(day, FMT)).days / 365

                c_50_str, c_50_settle, c_50_iv = get_row_text(opts, 0, "calls", t)
                c_15_str, c_15_settle, c_15_iv = get_row_text(opts, 1, "calls", t)
                c_05_str, c_05_settle, c_05_iv = get_row_text(opts, 2, "calls", t)
                
                p_50_str, p_50_settle, p_50_iv = get_row_text(opts, 0, "puts", t)
                p_15_str, p_15_settle, p_15_iv = get_row_text(opts, 1, "puts", t)
                p_05_str, p_05_settle, p_05_iv = get_row_text(opts, 2, "puts", t)

                print(
                    f"{day:12}",
                    f"{c_50_str:10.3f}{c_50_settle:10.3f}{c_50_iv:10.3f}",
                    f"{c_15_str:10.3f}{c_15_settle:10.3f}{c_15_iv:10.3f}",
                    f"{c_05_str:10.3f}{c_05_settle:10.3f}{c_05_iv:10.3f}",
                    f"{p_50_str:10.3f}{p_50_settle:10.3f}{p_50_iv:10.3f}",
                    f"{p_15_str:10.3f}{p_15_settle:10.3f}{p_15_iv:10.3f}",
                    f"{p_05_str:10.3f}{p_05_settle:10.3f}{p_05_iv:10.3f}"
                )

        print("\n\n")

if __name__ == "__main__":

    ul          = argv[1]
    opt_class   = argv[2]
    days        = argv[3]

    report(ul, opt_class, int(days))