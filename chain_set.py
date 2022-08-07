from chain_day import chain_day


# do not instantiate, call util.get_chain_set

class chain_set():


    def __init__(
        self, 
        symbol: str
    ):

        self.data  = None
        self.symbol = symbol

    
    def set_data(
        self,
        data: dict[str: dict[str: chain_day]]
    ):

        self.data   = data
        self.dates  = sorted(data.keys())

        for date in data:

            data[date]["expiries"] = sorted(data[date].keys())

    
    def get_dates(self):

        return self.dates

    
    def get_expiries_by_date(self, date: str):

        return self.data[date]["expiries"]


    def get_chain_day(self, date: str, expiry: str):

        return self.data[date][expiry]