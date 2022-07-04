

class chain_def():


    def __init__(
        self,
        opt_class:      str,
        underlying_id:  str,
        expiry:         str
    ):

        self.opt_class      = opt_class
        self.expiry         = expiry
        self.underlying_id  = underlying_id


    def __str__(self):

        return "\t".join(
            [
                self.opt_class,
                self.expiry,
                self.underlying_id
            ]
        )