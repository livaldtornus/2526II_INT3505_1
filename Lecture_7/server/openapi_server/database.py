import os
import uuid
from pymongo import MongoClient

# Configuration
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("DB_NAME", "product_db")
COLLECTION_NAME = "products"

# Initialize Client
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

def _format_product(doc):
    """Helper to convert MongoDB document to API format."""
    if not doc:
        return None
    # Use the 'id' field from document (which is our UUID string)
    return {
        "id": doc.get("id"),
        "name": doc.get("name"),
        "price": doc.get("price"),
        "description": doc.get("description"),
        "quantity": doc.get("quantity")
    }

def get_products():
    docs = collection.find()
    return [_format_product(doc) for doc in docs]

def get_product_by_id(product_id):
    doc = collection.find_one({"id": product_id})
    return _format_product(doc)

def create_product(product_data):
    new_product = {
        "id": str(uuid.uuid4()),
        "name": product_data.get("name"),
        "price": product_data.get("price"),
        "description": product_data.get("description", ""),
        "quantity": product_data.get("quantity", 0)
    }
    collection.insert_one(new_product)
    return _format_product(new_product)

def update_product(product_id, product_data):
    update_fields = {
        "name": product_data.get("name"),
        "price": product_data.get("price")
    }
    
    # Optional fields
    if "description" in product_data:
        update_fields["description"] = product_data["description"]
    if "quantity" in product_data:
        update_fields["quantity"] = product_data["quantity"]

    result = collection.find_one_and_update(
        {"id": product_id},
        {"$set": update_fields},
        return_document=True
    )
    return _format_product(result)

def delete_product(product_id):
    result = collection.delete_one({"id": product_id})
    return result.deleted_count > 0
