import unittest
import json
from app import create_app, db
from app.models import Mechanic

class MechanicTestCase(unittest.TestCase):
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

    def test_get_mechanics(self):
        response = self.client.get('/mechanics/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_create_mechanic_unauthorized(self):
        new_mechanic = {
            "name": "Alice Smith",
            "specialty": "Engine Repair",
            "phone": "9876543210"
        }
        response = self.client.post('/mechanics/', json=new_mechanic)
        self.assertEqual(response.status_code, 401)  # Unauthorized because no JWT token

    # Add more tests for GET by id, PUT, DELETE, including negative tests

if __name__ == '__main__':
    unittest.main()
