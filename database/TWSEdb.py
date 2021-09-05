import pymongo

stock_base_template = {
  "_id": 2603,
  "name": "",
  "number": "",
  "country": "TWSE",
  "listed": "",
  "currency": "NTD",
  "start_date": "",
  "industry": "",
  "decimal_no": 2,
  "prices": {}
}

price_data_template = {
      "date": "20210905",

      "high_p": 220.00,
      "low_p": 220.00,
      "start_p": 220.00,
      "end_p": 220.00,

      "trend": "UP, DOWN, EVEN",
      "type": "",
      "solid_range": 10.00,
      "dotted_range": 10.00,
      "amount": 2222220.00,
    }


class TWSEdb:

    my_client = None
    db_list = None
    my_db = None
    my_col = None

    def __init__(self, db: str, col: str):
        try:
            self.my_client = pymongo.MongoClient("mongodb://localhost:27017/")
            self.db_list = self.my_client.list_database_names()
            self.my_db = self.my_client[db]
            self.my_col = self.my_db[col]
        except Exception as e:
            print(e)

    def add_stock_info(self, stock_id: str, name: str = None, country: str = None, listed: str = None, start_date: str = None, industry: str = None, currency: str = None, decimal_no: int = None):  # todo: add more params
        try:
            update_data = stock_base_template
            update_data["_id"] = int(stock_id)
            update_data["number"] = stock_id
            if name is not None:
                update_data["str"] = name

            if country is not None:
                update_data["country"] = country
            else:
                update_data["country"] = "TWSE"

            if listed is not None:
                update_data["listed"] = listed

            if start_date is not None:
                update_data["start_date"] = start_date

            if industry is not None:
                update_data["industry"] = industry

            if currency is not None:
                update_data["currency"] = currency
            else:
                update_data["currency"] = "NTD"

            if decimal_no is not None:
                update_data["decimal_no"] = decimal_no
            else:
                update_data["decimal_no"] = 2

            self.my_col.insert_one(update_data)
            print("success to insertData")

        except Exception as e:
            print("fail to insertData")
            print(e)

    def update_stock_info(self, stock_id: int, name: str = None, number: int = None, listed: bool = None):
        try:
            if name is not None:
                self.my_col.update_one({"_id": stock_id}, {"$set": {"name": name}})
            if number is not None:
                self.my_col.update_one({"_id": stock_id}, {"$set": {"number": number}})
            if listed is not None:
                self.my_col.update_one({"_id": stock_id}, {"$set": {"listed": listed}})
        except Exception as e:
            print(f'Fail to update stock base data at id = "{stock_id}"')
            print(e)

    def update_price(self, date: int = None, high_p: int = None, low_p: int = None, start_p: int = None, end_p: int = None , amount: int = None):
        pass

    def add_price_data(self, stock_id: int, date: int, high_p: int, low_p: int, start_p: int, end_p: int, amount: int):
        new_data = price_data_template
        new_data["date"] = date
        new_data["high_p"] = high_p
        new_data["low_p"] = low_p
        new_data["start_p"] = start_p
        new_data["end_p"] = end_p
        new_data["amount"] = amount

        trend = ""

        if (end_p - start_p) > 0:
            trend = "UP"

        if (end_p - start_p) < 0:
            trend = "DOWN"

        if (end_p - start_p) == 0:
            trend = "EVEN"

        new_data["trend"] = trend

        solid_range = abs(end_p - start_p)
        dotted_range = abs(high_p - low_p)
        new_data["solid_range"] = solid_range
        new_data["dotted_range"] = dotted_range

        update_key = f'prices.{date}'

        try:
            self.my_col.update_one({"_id": stock_id}, {"$set": {update_key: new_data}})
        except Exception as e:
            print(f'Fail to add stock price data at id = "{stock_id}", date = "{date}"')
            print(e)
