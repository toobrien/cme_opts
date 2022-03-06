from util       import get_chain_defs_by_date, get_chain_day
from sys        import argv
from structs    import opt_row
from typing     import List


def report(underlyings: List):

    for underlying in underlyings:

        by_date = get_chain_defs_by_date(underlying)
        latest  = list(by_date.keys())[-1]
        
        for chain_def in by_date[latest]:

            # print(chain_def)

            cd = get_chain_day(chain_def, latest)

            print(cd)


if __name__ == "__main__":

    report(argv[1:])