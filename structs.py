from enum import IntEnum


class opt_row(IntEnum):

    date                = 0     # yyyy-mm-dd
    symbol              = 1     # option class e.g. "OZC" or "BZ0"
    strike              = 2     # float
    expiry              = 3     # yyyy-mm-dd
    call                = 4     # 1 for call, 0 for put
    last_traded         = 5     # yyyy-mm-dd
    settle              = 6     # float
    settle_delta        = 7     # float
    high_limit          = 8     # float
    low_limit           = 9     # float
    high_bid            = 10    # float
    low_bid             = 11    # float
    previous_volume     = 12    # int
    previous_interest   = 13    # int
    underlying_symbol   = 14    # "ZC", "CL", etc.
    underlying_exchange = 15    # "CBOT", "CME", "NYMEX, "ICE", etc.
    underlying_id       = 16    # e.g. "CBOT_ZCH2022"
