class Candlestick:

    date: int = None  # example: 20210904

    high_p: int = None
    low_p: int = None
    start_p: int = None
    end_p: int = None
    trend: str = None  # UP, DOWN , EVEN

    solid_range: int = None
    dotted_range: int = None

    amount: int = None

    def __init__(self):
        pass

    def set_price_amount(self, date, high_p, low_p, start_p, end_p, amount=None):
        self.date = int(date)
        self.high_p = int(high_p)
        self.low_p = int(low_p)
        self.start_p = int(start_p)
        self.end_p = int(end_p)
        self.amount = amount

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


