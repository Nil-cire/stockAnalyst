from .Candlestick import Candlestick


class Stock:

    candles: dict = {}  # list of Candlesticks
    country = None  # TWSE...
    number: str = None  #
    name: str = None  #
    date_period: list = []

    def __init__(self, country: str, number: str, name: str = None):
        self.country = country
        self.number = number
        self.name = name

    def set_candles(self, candles: "list of Candlestick"):

        for c in candles:
            if c is Candlestick:
                self.candles[c.date] = c
                self.date_period.append(c.date)
            else:
                "invalid candlestick data"
                return False

        return True

