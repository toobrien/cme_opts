from chain_day  import chain_day
from chain_def  import chain_def
from json       import loads
from sqlite3    import connect
from structs    import opt_row

CONFIG  = loads(open("./config.json").read())
CON     = connect(CONFIG["db_path"])
CUR     = CON.cursor()


def get_chain_defs_by_date(symbol: str):

    rows = CUR.execute(
        f'''
            SELECT      date, name, expiry, underlying_id, COUNT(1)
            FROM        cme_opts
            WHERE       underlying_symbol = "{symbol}"
            GROUP BY    date, name, expiry, underlying_id
            ORDER BY    date ASC, expiry ASC
        '''
    ).fetchall()

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


def get_chain_day(definition: chain_def, date: str):

    ul_row = CUR.execute(
        f'''
            SELECT  date, contract_id, year, month, settle
            FROM    ohlc
            WHERE   contract_id = "{definition.underlying_id}" AND date = "{date}"
        '''
    ).fetchall()[0]

    opt_rows = CUR.execute(
        f'''
            SELECT  *
            FROM    cme_opts
            WHERE   date            = "{date}"
            AND     name            = "{definition.name}"
            AND     expiry          = "{definition.expiry}"
            AND     underlying_id   = "{definition.underlying_id}"
        '''
    ).fetchall()

    cd = chain_day(
        date,
        definition.name,
        ul_row[3],
        ul_row[2],
        ul_row[4],
        ul_row[1]
    )

    cd.set_opt_rows(opt_rows)

    return cd