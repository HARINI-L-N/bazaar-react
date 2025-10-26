import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
uri = os.environ.get('MONGODB_URI') or os.environ.get('MONGO_URI') or os.environ.get('MONGO_URL') or 'mongodb://localhost:27017/bazaar'
if '/' in uri and uri.split('/')[-1]:
    db_name = uri.split('/')[-1]
else:
    db_name = 'bazaar'

client = MongoClient(uri)
db = client[db_name]

# Remove fields that conflict with MongoEngine Product schema
res1 = db.product.update_many({}, {'$unset': {'sku': '', 'seed_source': ''}})
res2 = db.products.update_many({}, {'$unset': {'sku': '', 'seed_source': ''}})
print(f"Matched {res1.matched_count}, modified {res1.modified_count} documents in 'product' collection.")
print(f"Matched {res2.matched_count}, modified {res2.modified_count} documents in 'products' collection.")

# Show total and a sample
print('Total in product collection:', db.product.count_documents({}))
print('Total in products collection:', db.products.count_documents({}))
print('Sample document keys:')
sample = db.product.find_one()
if sample:
    print(list(sample.keys()))
else:
    print('No sample found')
