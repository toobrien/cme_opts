from json       import loads
from util       import get_chain_defs_by_date, get_chain_day
from sys        import argv
from structs    import opt_row


# usage: python list_defs.py ZW all


CONTRACT_DESCRIPTIONS = loads(open("./contract_descriptions.json").read())


def report(ul: str, class_: str):


    by_date = get_chain_defs_by_date(ul)
    latest  = list(by_date.keys())[-1]
        
    for chain_def in by_date[latest]:

        if class_ == "all" or chain_def.opt_class == class_:

            cd = get_chain_day(chain_def, latest)
            oi = 0

            for _, rows in cd.opt_rows.items():

                try:    oi += rows[0][opt_row.previous_interest]
                except: pass

                try:    oi += rows[1][opt_row.previous_interest]
                except: pass

            print(str(chain_def) + "\t" + str(oi) + "\t" + CONTRACT_DESCRIPTIONS[chain_def.opt_class])


if __name__ == "__main__":

    ul      = argv[1]
    class_  = argv[2]

    report(ul, class_)