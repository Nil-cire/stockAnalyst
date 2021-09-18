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

    def form_candle_type(self) -> bool:
        if not self.is_data_verified():
            print("Price or amount not verified")
            return False

        if (self.end_p - self.start_p) > 0:
            self.trend = "UP"

        if (self.end_p - self.start_p) < 0:
            self.trend = "DOWN"

        if (self.end_p - self.start_p) == 0:
            self.trend = "EVEN"

        self.solid_range = abs(self.end_p - self.start_p)
        self.dotted_range = abs(self.high_p - self.low_p)

        return True


