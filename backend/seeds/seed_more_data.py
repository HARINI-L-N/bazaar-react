import os
import random
from datetime import datetime, timedelta
from pprint import pprint

from pymongo import MongoClient
from dotenv import load_dotenv

# Load .env if present (project root .env should contain MONGO_URI or similar)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

# Try environment variables commonly used in this repo
MONGO_URI = os.environ.get('MONGO_URI') or os.environ.get('MONGODB_URI') or os.environ.get('MONGO_URL') or "mongodb://localhost:27017"
DB_NAME = os.environ.get('MONGO_DBNAME') or os.environ.get('MONGO_DB') or os.environ.get('MONGO_DATABASE') or "bazaar"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

def clear_previous_seed():
    # Remove previously seeded docs (keeps production data safe if you use a different tag)
    db.products.delete_many({"seed_source": "bazaar-seed"})
    db.users.delete_many({"seed_source": "bazaar-seed"})
    db.events.delete_many({"seed_source": "bazaar-seed"})
    print("Cleared previous seed documents (if any).")

def seed_products():
    products = [
        {"sku": "ELEC-001", "name": "Wireless Headphones Pro", "category": "electronics",
         "description": "Noise cancelling over-ear headphones with 30h battery.", "tags": ["audio","headphones","wireless"],
         "price": 129.99, "seed_source": "bazaar-seed"},
        {"sku": "ELEC-002", "name": "Smartphone X200", "category": "electronics",
         "description": "6.5\" display, 128GB, dual camera.", "tags": ["phone","mobile","camera"],
         "price": 499.00, "seed_source": "bazaar-seed"},
        {"sku": "HOME-001", "name": "Memory Foam Pillow", "category": "home",
         "description": "Ergonomic memory foam pillow for better sleep.", "tags": ["sleep","bedroom","comfort"],
         "price": 39.50, "seed_source": "bazaar-seed"},
        {"sku": "FASH-001", "name": "Classic Denim Jacket", "category": "fashion",
         "description": "Unisex denim jacket, multiple sizes.", "tags": ["jacket","denim","clothing"],
         "price": 79.00, "seed_source": "bazaar-seed"},
        {"sku": "BOOK-001", "name": "Modern Python Cookbook", "category": "books",
         "description": "Recipes and patterns for modern Python development.", "tags": ["programming","python","book"],
         "price": 24.99, "seed_source": "bazaar-seed"},
        {"sku": "SPORT-001", "name": "Running Shoes LX", "category": "sports",
         "description": "Lightweight running shoes with breathable mesh.", "tags": ["shoes","running","exercise"],
         "price": 89.99, "seed_source": "bazaar-seed"},
        {"sku": "BEAU-001", "name": "Vitamin C Serum", "category": "beauty",
         "description": "Brightening face serum, 30ml.", "tags": ["skincare","serum","beauty"],
         "price": 19.99, "seed_source": "bazaar-seed"},
        {"sku": "ELEC-003", "name": "4K Action Camera", "category": "electronics",
         "description": "Rugged action cam with 4K and waterproof body.", "tags": ["camera","action","outdoors"],
         "price": 149.00, "seed_source": "bazaar-seed"},
        {"sku": "HOME-002", "name": "Stainless Steel Kettle", "category": "home",
         "description": "Fast-boil electric kettle, 1.7L.", "tags": ["kitchen","appliance","tea"],
         "price": 29.99, "seed_source": "bazaar-seed"},
        {"sku": "FASH-002", "name": "Running Shorts", "category": "fashion",
         "description": "Moisture-wicking shorts for sports.", "tags": ["clothing","running","sportswear"],
         "price": 25.00, "seed_source": "bazaar-seed"},
        {"sku": "BOOK-002", "name": "Beginner's Guide to Photography", "category": "books",
         "description": "Understand exposure, composition and lighting.", "tags": ["photography","hobby","book"],
         "price": 18.50, "seed_source": "bazaar-seed"},
        {"sku": "TOY-001", "name": "Wooden Puzzle Set", "category": "toys",
         "description": "Educational wooden puzzles for ages 3+.", "tags": ["kids","educational","wooden"],
         "price": 15.00, "seed_source": "bazaar-seed"},
        {"sku": "SPORT-002", "name": "Yoga Mat Pro", "category": "sports",
         "description": "Non-slip yoga mat with carry strap.", "tags": ["yoga","fitness","mat"],
         "price": 29.95, "seed_source": "bazaar-seed"},
        {"sku": "ELEC-004", "name": "Bluetooth Speaker Cube", "category": "electronics",
         "description": "Portable speaker with 12h playtime.", "tags": ["audio","speaker","portable"],
         "price": 45.00, "seed_source": "bazaar-seed"},
        {"sku": "BEAU-002", "name": "Scented Candle - Lavender", "category": "home",
         "description": "Relaxing lavender scented candle, 250g.", "tags": ["candle","relax","aroma"],
         "price": 12.00, "seed_source": "bazaar-seed"},
    ]

    result = db.products.insert_many(products)
    print(f"Inserted {len(result.inserted_ids)} products.")
    return result.inserted_ids

def seed_users(product_ids):
    names = [
        ("Alice", "alice@example.com"),
        ("Bob", "bob@example.com"),
        ("Carla", "carla@example.com"),
        ("David", "david@example.com"),
        ("Eva", "eva@example.com"),
        ("Frank", "frank@example.com"),
        ("Gina", "gina@example.com"),
        ("Henry", "henry@example.com"),
        ("Iris", "iris@example.com"),
        ("John", "john@example.com"),
    ]

    users = []
    for i, (name, email) in enumerate(names):
        # give each user some categories of interest and some initially viewed products
        preferred_categories = random.sample(["electronics", "fashion", "home", "books", "sports", "beauty", "toys"], k=2)
        # sample some product object ids for viewed list
        viewed = random.sample(list(product_ids), k=min(6, len(product_ids)))
        users.append({
            "username": name.lower(),
            "name": name,
            "email": email,
            "preferred_categories": preferred_categories,
            "viewed_products": viewed,
            "purchase_history": [],  # can be appended later by events
            "created_at": datetime.utcnow(),
            "seed_source": "bazaar-seed"
        })

    result = db.users.insert_many(users)
    print(f"Inserted {len(result.inserted_ids)} users.")
    return result.inserted_ids

def seed_events(user_ids, product_ids, days=30):
    events = []
    now = datetime.utcnow()

    # create many simulated view events to support collaborative filtering
    for u in user_ids:
        # each user generates between 20-60 events across time
        event_count = random.randint(20, 60)
        for _ in range(event_count):
            product_id = random.choice(list(product_ids))
            # random time within last `days`
            ts = now - timedelta(days=random.uniform(0, days), hours=random.uniform(0, 24))
            events.append({
                "user_id": u,
                "product_id": product_id,
                "event_type": random.choices(["view", "add_to_cart", "purchase"], weights=[0.75, 0.20, 0.05])[0],
                "timestamp": ts,
                "metadata": {},
                "seed_source": "bazaar-seed"
            })

    inserted = db.events.insert_many(events)
    print(f"Inserted {len(inserted.inserted_ids)} events.")
    return inserted.inserted_ids


def main():
    clear_previous_seed()
    product_obj_ids = seed_products()
    user_obj_ids = seed_users(product_obj_ids)
    seed_events(user_obj_ids, product_obj_ids)
    print("Seeding complete. Sample documents:")
    print("Product sample:")
    pprint(db.products.find_one({"seed_source": "bazaar-seed"}))
    print("User sample:")
    pprint(db.users.find_one({"seed_source": "bazaar-seed"}))
    print("Event sample:")
    pprint(db.events.find_one({"seed_source": "bazaar-seed"}))


if __name__ == "__main__":
    main()
