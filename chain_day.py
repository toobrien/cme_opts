from structs    import opt_row
from typing     import List
from bisect     import bisect_left


# do not instantiate, call util.get_chain_day

class chain_day():


    def __init__(
        self, 
        date:               str,
        symbol:             str,
        underlying_month:   str,
        underlying_year:    str,
        underlying_settle:  float,
        underlying_id:      str
    ):

        self.date               = date
        self.symbol             = symbol
        self.underlying_month   = underlying_month
        self.underlying_year    = underlying_year
        self.underlying_settle  = underlying_settle
        self.underlying_id      = underlying_id
        self.opt_rows           = {}
        self.strikes            = []
        self.call_deltas        = []
        self.put_deltas         = []


    def __str__(self):

        return  "\t".join(
            [
                self.date,
                self.symbol,
                self.underlying_id,
                self.underlying_month,
                f"{self.underlying_settle: 0.1f}",
                self.underlying_id,
                str(len(self.strikes))
            ]
        )


    def get_opt_by_delta(
        self, 
        call:   bool,
        delta:  float
    ):

        opt     = None
        deltas  = None
        side    = None     

        if call:

            deltas  = self.call_deltas
            side    = 1

        else:

            deltas  = self.put_deltas
            side    = 0

        nearest = bisect_left(deltas, delta)
        strike  = self.strikes[nearest]
        opt     = self.opt_rows[strike][side]

        '''
        for i in range(1, len(deltas)):

            if deltas[i - 1] >= delta and deltas[i] < delta:

                strike  = self.strikes[i]
                opt     = self.opt_rows[strike][side]
        '''

        return opt


    def get_opt_by_strike(
        self,
        call:   bool,
        strike: float
    ):

        opt     = None
        side    = 1 if call else 0

        nearest = bisect_left(self.strikes, strike)
        opt = self.opt_rows[nearest][side]

        return opt

    
    def get_atm_strikes(self, num_strikes: int):

        atm_idx = self.get_atm_idx()
        lo      = max(atm_idx - num_strikes, 0)
        hi      = atm_idx + num_strikes

        strikes = {}

        for strike in self.strikes[lo:hi]:

            strikes[strike] = self.opt_rows[strike]

        return strikes


    def get_strike_by_idx(self, idx: int):

        return self.opt_rows[self.strikes[idx]]


    def get_atm_idx(self):

        if self.strikes:

            return bisect_left(self.strikes, self.underlying_settle)
        
        else:

            return -1


    def set_opt_rows(self, rows: List[opt_row]): 
        
        opt_rows = self.opt_rows

        for row in rows:

            strike = row[opt_row.strike]

            if strike not in opt_rows:

                opt_rows[strike] = {}

            opt_rows[strike][row[opt_row.call]] = row

        self.strikes = list(opt_rows.keys())
        
        self.call_deltas  = [
            row[opt_row.settle_delta]
            for row in rows
            if row[opt_row.call]
        ]

        self.put_deltas = [
            row[opt_row.settle_delta]
            for row in rows
            if not row[opt_row.call]
        ]