import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load the backend .env so we inspect the same connection settings the seeder/app use
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

uri = os.environ.get('MONGODB_URI') or os.environ.get('MONGO_URI') or os.environ.get('MONGO_URL') or 'mongodb://localhost:27017/bazaar'
print('MONGODB_URI =', uri)

# derive db name
if '/' in uri and uri.split('/')[-1]:
    db_name = uri.split('/')[-1]
else:
    db_name = 'bazaar'
print('DB_NAME =', db_name)

client = MongoClient(uri)
db = client[db_name]
print('total_products =', db.products.count_documents({}))
print("seeded_bazaar_seed =", db.products.count_documents({'seed_source':'bazaar-seed'}))

# Print a sample id list sizes
print('sample 5 seeded _ids:')
for doc in db.products.find({'seed_source':'bazaar-seed'}).limit(5):
    print('-', doc.get('_id'))
print('\n')
print('distinct seed_source present:', db.products.distinct('seed_source')[:10])

# Also check the collection name used by MongoEngine (singular) if present
try:
    print('\nproduct (singular) collection count =', db.product.count_documents({}))
    print('sample product (singular) _ids:')
    for doc in db.product.find().limit(5):
        print('-', doc.get('_id'))
except Exception as e:
    print('Could not access singular product collection:', str(e))
