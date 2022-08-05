from chain_day import chain_day


# do not instantiate, call util.get_chain_set

class chain_set():


    def __init__(
        self, 
        symbol: str
    ):

        self.dates  = {}
        self.symbol = symbol

    
    def set_dates(
        self,
        dates: dict[str: dict[str: chain_day]]
    ):

        self.dates = dates