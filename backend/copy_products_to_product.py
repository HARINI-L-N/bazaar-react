import os
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime

# Load backend env
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

uri = os.environ.get('MONGODB_URI') or os.environ.get('MONGO_URI') or os.environ.get('MONGO_URL') or 'mongodb://localhost:27017/bazaar'
if '/' in uri and uri.split('/')[-1]:
    db_name = uri.split('/')[-1]
else:
    db_name = 'bazaar'

client = MongoClient(uri)
db = client[db_name]

source_coll = db.products
target_coll = db.product

count_inserted = 0
for doc in source_coll.find():
    # Avoid copying documents that already exist in target by name
    name = doc.get('name')
    if target_coll.find_one({'name': name}):
        continue
    # Prepare a new doc mapping fields expected by Product model
    new_doc = {
        'name': doc.get('name'),
        'description': doc.get('description', ''),
        'price': float(doc.get('price') or 0.0),
        'category': doc.get('category') or 'uncategorized',
        'tags': doc.get('tags', []),
        'features': doc.get('features', []),
        'image_url': doc.get('image_url') or doc.get('image'),
        'stock_quantity': int(doc.get('stock_quantity') or doc.get('stock') or 0),
        'rating': float(doc.get('rating') or 0.0),
        'review_count': int(doc.get('review_count') or 0),
        'is_active': bool(doc.get('is_active', True)),
        'created_at': doc.get('created_at') or datetime.utcnow(),
        'updated_at': doc.get('updated_at') or datetime.utcnow(),
    }
    target_coll.insert_one(new_doc)
    count_inserted += 1

print(f'Inserted {count_inserted} documents into "product" collection.')
print('New total in product collection:', target_coll.count_documents({}))
