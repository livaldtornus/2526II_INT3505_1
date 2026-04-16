import connexion
from typing import Dict, List, Tuple, Union

from openapi_server.models.product import Product  # noqa: E501
from openapi_server.models.product_input import ProductInput  # noqa: E501
from openapi_server import util
from openapi_server import database

def create_product(body=None):  # noqa: E501
    """Create a new product
    """
    if connexion.request.is_json:
        data = connexion.request.get_json()
        new_product_data = database.create_product(data)
        return Product.from_dict(new_product_data), 201
    return "Invalid input", 400


def delete_product(id):  # noqa: E501
    """Delete a product
    """
    success = database.delete_product(id)
    if success:
        return None, 204
    return "Product not found", 404


def get_product(id):  # noqa: E501
    """Get a product by ID
    """
    product_data = database.get_product_by_id(id)
    if product_data:
        return Product.from_dict(product_data), 200
    return "Product not found", 404


def list_products():  # noqa: E501
    """List all products
    """
    products_data = database.get_products()
    return [Product.from_dict(p) for p in products_data], 200


def update_product(id, body=None):  # noqa: E501
    """Update a product
    """
    if connexion.request.is_json:
        data = connexion.request.get_json()
        updated_product_data = database.update_product(id, data)
        if updated_product_data:
            return Product.from_dict(updated_product_data), 200
        return "Product not found", 404
    return "Invalid input", 400
