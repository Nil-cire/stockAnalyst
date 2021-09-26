class Candlestick:

    date: int = None  # example: 20210904

    high_p: float = None
    low_p: float = None
    start_p: float = None
    end_p: float = None
    trend: str = None  # UP, DOWN , EVEN

    solid_range: float = None
    dotted_range: float = None

    amount: int = None

    ma5 = None
    ma10 = None
    ma14 = None
    ma20 = None
    ma21 = None
    ma60 = None
    ma120 = None
    ma150 = None
    ma240 = None

    boll_high = None
    boll_mid = None
    boll_low = None

    obv = None

    rsi5 = None
    rsi10 = None
    rsi14 = None
    rsi20 = None

    def __init__(self):
        pass

    def set_price_amount(self, date, high_p, low_p, start_p, end_p, amount=None, trend: str = None):
        self.date = date
        self.high_p = high_p
        self.low_p = low_p
        self.start_p = start_p
        self.end_p = end_p
        self.amount = amount
        self.trend = trend
        return self

    def set_ma(self, ma5, ma10, ma14, ma20, ma21, ma60, ma120, ma150, ma240):
        self.ma5 = ma5
        self.ma10 = ma10
        self.ma14 = ma14
        self.ma20 = ma20
        self.ma21 = ma21
        self.ma60 = ma60
        self.ma120 = ma120
        self.ma150 = ma150
        self.ma240 = ma240
        return self

    def set_bollinger(self, boll_high, boll_mid, boll_low):
        self.boll_high = boll_high
        self.boll_mid = boll_mid
        self.boll_low = boll_low
        return self

    def set_obv(self, obv):
        self.obv = obv
        return self

    def set_rsi(self, rsi5, rsi10, rsi14, rsi20):
        self.rsi5 = rsi5
        self.rsi10 = rsi10
        self.rsi14 = rsi14
        self.rsi20 = rsi20
        return self

    def is_data_verified(self):
        if self.date is None:
            print("Data: date, not set")
            return False

        if self.high_p is None:
            print("Data: high_p, not set")

            return False

        if self.low_p is None:
            print("Data: low_p, not set")
            return False

        if self.start_p is None:
            print("Data: start_p, not set")
            return False

        if self.end_p is None:
            print("Data: end_p, not set")
            return False

        if self.amount is None:
            print("Data: amount, not set")
            return False

    def set_candle_type(self):
        # if not self.is_data_verified():
        #     print("Price or amount not verified")
        #     return False

        if (self.end_p - self.start_p) > 0:
            self.trend = "UP"

        if (self.end_p - self.start_p) < 0:
            self.trend = "DOWN"

        if (self.end_p - self.start_p) == 0:
            self.trend = "EVEN"

        self.solid_range = round(abs(self.end_p - self.start_p), 2)
        self.dotted_range = round(abs(self.high_p - self.low_p), 2)

        return self


