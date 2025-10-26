"""Seed script — insert 50+ realistic products into the products collection.

Usage:
  python seed_products.py

This script uses the same MongoDB URI as the Flask backend (reads MONGODB_URI from .env).
It uses pymongo and faker to generate realistic product docs. The products include fields
expected by the backend Product model: name, category, description, price, rating,
image_url, specs (dict), tags (list), review_count, stock_quantity, is_active, created_at,
updated_at and a "seed_source" tag so seeded documents can be identified and removed.

If the products collection already has documents, the script will skip seeding to avoid
accidentally duplicating production data.

Requirements:
  pip install pymongo faker python-dotenv

"""

import os
import random
from datetime import datetime, timedelta
from pprint import pprint

import argparse
from faker import Faker
from pymongo import MongoClient
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(__file__)
# Load project .env (one level up if you keep env at repo root)
load_dotenv(os.path.join(BASE_DIR, '.env'))
load_dotenv(os.path.join(BASE_DIR, '..', '.env'))

MONGO_URI = os.environ.get('MONGODB_URI') or os.environ.get('MONGO_URI') or os.environ.get('MONGO_URL') or 'mongodb://localhost:27017/bazaar'
# If URI contains a database at the end, use it; otherwise default to 'bazaar'
DB_NAME = os.environ.get('MONGO_DBNAME') or os.environ.get('MONGO_DB') or (MONGO_URI.split('/')[-1] if '/' in MONGO_URI and MONGO_URI.split('/')[-1] else 'bazaar')

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

fake = Faker()
Faker.seed(42)
random.seed(42)

CATEGORIES = [
    'Laptops', 'Smartphones', 'Headphones', 'Smartwatches', 'Accessories', 'Home Appliances', 'Cameras', 'Gaming', 'Audio', 'Kitchen'
]
BRANDS = ['Apple', 'Samsung', 'Lenovo', 'Sony', 'OnePlus', 'Asus', 'Dell', 'HP', 'Xiaomi', 'Google']
IMAGE_HOST = 'https://picsum.photos/seed'

# Helper to generate specs depending on category
def gen_specs(category):
    specs = {}
    if category == 'Laptops':
        specs = {
            'cpu': random.choice(['Intel i5', 'Intel i7', 'Intel i9', 'AMD Ryzen 5', 'AMD Ryzen 7']),
            'ram': f"{random.choice([8,16,32])}GB",
            'storage': f"{random.choice([256,512,1024])}GB SSD",
            'screen': f"{random.choice([13,14,15,16])} inch",
            'weight': f"{random.uniform(1.0,2.5):.1f} kg"
        }
    elif category == 'Smartphones':
        specs = {
            'screen': f"{random.choice([5.8,6.1,6.4,6.7])} inch OLED",
            'ram': f"{random.choice([6,8,12])}GB",
            'storage': f"{random.choice([64,128,256,512])}GB",
            'battery': f"{random.choice([3000,4000,4500,5000])} mAh",
            'camera': f"{random.choice([12,48,64,108])}MP"
        }
    elif category == 'Headphones':
        specs = {
            'type': random.choice(['Over-Ear', 'In-Ear', 'On-Ear']),
            'connectivity': random.choice(['Bluetooth', 'Wired', 'Wireless']),
            'battery_life': f"{random.choice([15,20,30,40])} hours",
            'noise_cancelling': random.choice([True, False])
        }
    elif category == 'Smartwatches':
        specs = {
            'display': random.choice(['AMOLED','LCD']),
            'battery': f"{random.choice([24,48,72])} hours",
            'water_resistant': random.choice(['5 ATM','3 ATM','IP68']),
        }
    elif category == 'Home Appliances':
        specs = {
            'power': f"{random.choice([800,1200,1500,2000])}W",
            'capacity': random.choice(['1.5L','1.7L','2.0L','5L','20L']),
            'material': random.choice(['Stainless Steel','Plastic','Glass'])
        }
    elif category == 'Cameras':
        specs = {
            'resolution': f"{random.choice([20,24,30,45,50])}MP",
            'sensor': random.choice(['APS-C','Full Frame','Micro Four Thirds']),
            'video': random.choice(['4K','1080p','6K'])
        }
    else:
        # Generic specs for accessories/gaming/kitchen
        specs = {
            'feature_1': fake.word(),
            'feature_2': fake.word()
        }
    return specs

# Build tags from specs + category
def build_tags(category, specs):
    tags = set()
    # base tags from category
    tags.add(category.lower())
    # add brand/feature tags
    for v in specs.values():
        if isinstance(v, bool):
            tags.add('noise-cancelling' if v else 'no-nc')
        elif isinstance(v, str):
            for part in v.replace('-', ' ').split():
                if len(part) > 1 and not part.isdigit():
                    tags.add(part.lower())
    # add some standard tags
    tags.update(random.sample(['wireless','portable','battery','fast-charging','bestseller','budget','premium','new'], 2))
    # ensure 2-5 tags
    tags_list = list(tags)
    random.shuffle(tags_list)
    return tags_list[:random.randint(2,5)]


def generate_product(index):
    brand = random.choice(BRANDS)
    category = random.choice(CATEGORIES)
    model_token = fake.lexify(text='??-####').upper()
    name = f"{brand} {model_token} {random.choice(['Pro','X','S','Lite','Max','Plus'])}"
    description = fake.sentence(nb_words=18) + ' ' + fake.paragraph(nb_sentences=2)
    price = round(random.uniform(49.0, 2499.0), 2)
    # weight ratings towards 4.0-4.8 but include some lower/higher
    rating = round(random.normalvariate(4.2, 0.5), 1)
    rating = max(1.0, min(5.0, rating))
    review_count = random.randint(0, 5000)
    image_url = f"{IMAGE_HOST}/{index}?w=500&h=500"
    specs = gen_specs(category)
    tags = build_tags(category, specs)
    # occasionally mark some as bestseller
    if random.random() < 0.12:
        tags.append('bestseller')
        rating = min(5.0, round(max(rating, random.uniform(4.3, 5.0)),1))
        review_count += random.randint(100, 2000)
    created_at = datetime.utcnow() - timedelta(days=random.randint(0, 365))
    updated_at = created_at + timedelta(days=random.randint(0, 90))
    stock_quantity = random.randint(0, 200)

    doc = {
        'name': name,
        'category': category,
        'description': description,
        'price': price,
        'rating': rating,
        'review_count': review_count,
        'image_url': image_url,
        'specs': specs,
        'tags': tags,
        'stock_quantity': stock_quantity,
        'is_active': True,
        'created_at': created_at,
        'updated_at': updated_at,
        'seed_source': 'seed_products_v1'
    }
    return doc


def seed_products(count=60):
    products_coll = db.products

    # Only treat previously-seeded documents from this script as blocking.
    # This prevents accidental skips when the collection already contains other data.
    existing_seeded = products_coll.count_documents({'seed_source': 'seed_products_v1'})
    if existing_seeded > 0 and not getattr(seed_products, '_force', False):
        print(f"Found {existing_seeded} products with seed_source 'seed_products_v1' — skipping. Use --force to re-seed.")
        return 0

    # If force reseed was requested, remove previous seed_products_v1 docs only
    if getattr(seed_products, '_force', False):
        removed = products_coll.delete_many({'seed_source': 'seed_products_v1'})
        print(f"Removed {removed.deleted_count} existing 'seed_products_v1' documents before reseed.")

    docs = [generate_product(i) for i in range(1, count + 1)]
    result = products_coll.insert_many(docs)
    inserted = len(result.inserted_ids)
    print(f"Inserted {inserted} products into {DB_NAME}.products")
    return inserted


def main():
    parser = argparse.ArgumentParser(description='Seed products into MongoDB (seed_products_v1)')
    parser.add_argument('--count', type=int, default=60, help='Number of products to generate')
    parser.add_argument('--force', action='store_true', help='Force reseed: delete previous seed_products_v1 docs and insert fresh set')
    args = parser.parse_args()

    # Expose force flag to seed_products via attribute to avoid changing many signatures
    setattr(seed_products, '_force', args.force)

    print(f"Connecting to MongoDB: {MONGO_URI} (DB: {DB_NAME})")
    try:
        inserted = seed_products(args.count)
        if inserted:
            sample = db.products.find_one({'seed_source': 'seed_products_v1'})
            print('Sample document:')
            pprint(sample)
    except Exception as e:
        print('Seeding failed:', str(e))


if __name__ == '__main__':
    main()
