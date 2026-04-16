import unittest

from flask import json

from openapi_server.models.product import Product  # noqa: E501
from openapi_server.models.product_input import ProductInput  # noqa: E501
from openapi_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_create_product(self):
        """Test case for create_product

        Create a new product
        """
        product_input = {"quantity":6,"price":0.8008281904610115,"name":"name","description":"description"}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/v1/products',
            method='POST',
            headers=headers,
            data=json.dumps(product_input),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_product(self):
        """Test case for delete_product

        Delete a product
        """
        headers = { 
        }
        response = self.client.open(
            '/v1/products/{id}'.format(id='id_example'),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_product(self):
        """Test case for get_product

        Get a product by ID
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/v1/products/{id}'.format(id='id_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_products(self):
        """Test case for list_products

        List all products
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/v1/products',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_product(self):
        """Test case for update_product

        Update a product
        """
        product_input = {"quantity":6,"price":0.8008281904610115,"name":"name","description":"description"}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/v1/products/{id}'.format(id='id_example'),
            method='PUT',
            headers=headers,
            data=json.dumps(product_input),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
