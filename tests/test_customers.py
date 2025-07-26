import unittest
import json
from app import create_app, db
from app.models import Customer
from flask_jwt_extended import create_access_token

class CustomersTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app().test_client()
        self.access_token = None

        with create_app().app_context():
            db.create_all()
            self.access_token = create_access_token(identity="admin")

    def tearDown(self):
        with create_app().app_context():
            db.drop_all()

    def test_create_customer_success(self):
        new_customer = {
            "name": "Test Customer",
            "email": "test@example.com",
            "phone": "1234567890"
        }
        response = self.app.post('/customers/',
                                 data=json.dumps(new_customer),
                                 content_type='application/json',
                                 headers={"Authorization": f"Bearer {self.access_token}"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], new_customer['name'])
