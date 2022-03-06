from enum import IntEnum


class opt_row(IntEnum):

    date                = 0
    symbol              = 1
    strike              = 2
    expiry              = 3
    call                = 4
    last_traded         = 5
    settle              = 6
    settle_delta        = 7
    high_limit          = 8
    low_limit           = 9
    high_bid            = 10
    low_bid             = 11
    previous_volume     = 12
    previous_interest   = 13
    underlying_symbol   = 14
    underlying_exchange = 15
    underlying_id       = 16
