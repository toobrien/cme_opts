from    chain_day   import  chain_day
from    chain_def   import  chain_def
from    chain_set   import  chain_set
from    json        import  loads
import  polars      as      pl
from    structs     import  opt_row
from    time        import  time
from    typing      import  List


CONFIG  = loads(open("./config.json").read())
DB      = pl.SQLContext()

DB.register("cme_opts", pl.read_parquet(CONFIG["opts_path"]).lazy())
DB.register("ohlc", pl.read_parquet(CONFIG["futs_path"]).lazy())


# see list_defs.py for usage

def get_chain_defs_by_date(symbol: str):

    rows = DB.query(
        f'''
            SELECT DISTINCT date, name, expiry, underlying_id
            FROM            cme_opts
            WHERE           underlying_symbol = '{symbol}'
            ORDER BY        date ASC, expiry ASC;
        '''
    ).rows()

    # weird hack, "DISTINCT" not working in query above... need to fix

    rows = sorted(list(set(rows)), key = lambda x: (x[0], x[2]))

    by_date = {}

    for row in rows:

        date = row[0]

        if row[0] not in by_date:

            by_date[date] = []

        by_date[date].append(
            chain_def(
                row[1],
                row[3],
                row[2]
            )
        )

    return by_date


# see daily.py for usage

def get_chain_day(definition: chain_def, date: str):

    ul_row = None

    try:

        ul_row = DB.query(
            f'''
                SELECT  date, contract_id, year, month, settle
                FROM    ohlc
                WHERE   contract_id = '{definition.underlying_id}' AND date = '{date}'
            '''
        ).rows()[0]

    except IndexError:

        # no data for underlying on given date

        return None

    opt_rows = DB.query(
        f'''
            SELECT  *
            FROM    cme_opts
            WHERE   date            = '{date}'
            AND     name            = '{definition.opt_class}'
            AND     expiry          = '{definition.expiry}'
            AND     underlying_id   = '{definition.underlying_id}'
        '''
    ).rows()

    cd = chain_day(
        date,
        definition.opt_class,
        opt_rows[0][opt_row.expiry],
        ul_row[3],
        ul_row[2],
        ul_row[4],
        ul_row[1]
    )

    cd.set_opt_rows(opt_rows)

    return cd


# see history.py for usage

def get_expiries_for_underlying_and_class(
    underlying_id:  str, 
    opt_class:      str, 
    date:           str
):

    exps = DB.query(
        f'''
            SELECT      expiry
            FROM        cme_opts
            WHERE       date            = '{date}'
            AND         name            = '{opt_class}'
            AND         underlying_id   = '{underlying_id}'
            GROUP BY    expiry
        '''
    ).rows()

    flat = [ exp[0] for exp in exps ]

    return flat


# assumes no two options for a symbol expire on the same day
# if this is not correct, choose opt classes to exclude with "exclude_classes" until the assumption is valid

def get_chain_set(
    symbol:             str,
    start:              str,
    end:                str,
    excluded_classes:   List[str]
):

    cs = chain_set(symbol)

    t1 = time()

    opt_rows = DB.query(
        f'''
            SELECT  *
            FROM    cme_opts
            WHERE   date BETWEEN '{start}' AND '{end}'
            AND     underlying_symbol = '{symbol}'
            AND     name NOT IN ({', '.join(excluded_classes)})
        '''
    ).rows()

    # print(f"cs.get_chain_set:query: {time() - t1:0.1f}")

    dates = { row[opt_row.date]: {} for row in opt_rows }

    for row in opt_rows:

        date            = row[opt_row.date]
        symbol          = row[opt_row.symbol]
        ul_id           = row[opt_row.underlying_id]
        expiry          = row[opt_row.expiry]
        chain_def_id    = (symbol, ul_id, expiry)

        if expiry not in dates[date]:

            ch_def              = chain_def(*chain_def_id)
            dates[date][expiry] = get_chain_day(ch_def, date)

    cs.set_data(dates)

    return cs