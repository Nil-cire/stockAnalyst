from twsecrawler import ref
import pymongo

# listed_dict = ref.get_listed_stocks_info()
unlisted_dict = ref.get_unlisted_stocks_info()
db_name = "unlisted_stocks"

my_client = pymongo.MongoClient("mongodb://localhost:27017/")
# db_list = self.my_client.list_database_names()
my_db = my_client["stock_twse"]
my_col = my_db[db_name]

for key in unlisted_dict:
    if len(key) < 5:
        value = unlisted_dict[key]
        mock = {"name": value[1], "listed": value[3], "start_date": value[2], "industry": value[4]}
        update_key = f'stocks.{key}'
        my_col.update_one({"_id": 1}, {"$set": {update_key: mock}})



