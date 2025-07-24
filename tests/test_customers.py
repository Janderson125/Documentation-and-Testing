import unittest
import json
from app import create_app, db
from app.models import Customer

class CustomerTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def test_create_customer(self):
        new_customer = {
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "1234567890"
        }
        response = self.client.post('/customers/', json=new_customer)
        self.assertEqual(response.status_code, 401)  # Unauthorized because no JWT token

    def test_get_customers(self):
        response = self.client.get('/customers/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    # Add more tests for GET by id, PUT, DELETE, including negative tests

if __name__ == '__main__':
    unittest.main()
