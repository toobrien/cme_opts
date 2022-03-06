

class chain_def():


    def __init__(
        self,
        name:           str,
        underlying_id:  str,
        expiry:         str
    ):

        self.name         = name
        self.expiry         = expiry
        self.underlying_id  = underlying_id


    def __str__(self):

        return "\t".join(
            [
                self.name,
                self.expiry,
                self.underlying_id
            ]
        )