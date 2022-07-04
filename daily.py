from util       import get_chain_defs_by_date, get_chain_day
from sys        import argv
from structs    import opt_row


def report(
    ul: str,
    opt_class: str,
    n_strikes: int
):


    by_date = get_chain_defs_by_date(ul)
    latest  = list(by_date.keys())[-1]
        
    print(latest + "\n")

    for chain_def in by_date[latest]:

        if chain_def.opt_class == opt_class:
        
            cd = get_chain_day(chain_def, latest)

            print(
                f"{cd.underlying_id}".rjust(12), 
                f"{cd.underlying_settle: 0.2f}".rjust(12),
                "\n"
            )

            atm_strikes = cd.get_atm_strikes(n_strikes)
            idx         = list(atm_strikes.keys())
            idx.reverse()

            print(
                "strike".rjust(12),
                "call $".rjust(12),
                "call delta".rjust(12),
                "call int".rjust(12),
                "call vol".rjust(12),
                "put $".rjust(12),
                "put delta".rjust(12),
                "put oi".rjust(12),
                "put vol".rjust(12),
                "\n"
            )

            for strike in idx:
                
                try:
                
                    put     = atm_strikes[strike][0]

                except KeyError:

                    put = [ 0 ] * 16

                try:
                
                    call    = atm_strikes[strike][1] 

                except KeyError:

                    call = [ 0 ] * 16

                print(
                    f"{strike: 0.1f}".rjust(12),
                    f"{call[opt_row.settle]: 0.2f}".rjust(12),
                    f"{call[opt_row.settle_delta]: 0.2f}".rjust(12),
                    f"{call[opt_row.previous_interest]}".rjust(12),
                    f"{call[opt_row.previous_volume]}".rjust(12),
                    f"{put[opt_row.settle]: 0.2f}".rjust(12),
                    f"{put[opt_row.settle_delta]: 0.2f}".rjust(12),
                    f"{put[opt_row.previous_interest]}".rjust(12),
                    f"{put[opt_row.previous_volume]}".rjust(12),
                )
            
            print("\n")



if __name__ == "__main__":

    ul          = argv[1]
    opt_class    = argv[2]
    n_strikes   = int(argv[3])

    report(ul, opt_class, n_strikes)