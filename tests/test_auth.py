import unittest
import json
from app import create_app  # Assuming you have a create_app factory function

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app().test_client()

    def test_login_success(self):
        response = self.app.post('/auth/login', 
                                 data=json.dumps({"username": "admin", "password": "password123"}),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.json)

    def test_login_fail_wrong_password(self):
        response = self.app.post('/auth/login', 
                                 data=json.dumps({"username": "admin", "password": "wrongpass"}),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json.get('msg'), 'Bad username or password')

    def test_login_fail_missing_fields(self):
        response = self.app.post('/auth/login', 
                                 data=json.dumps({"username": "admin"}),
                                 content_type='application/json')
        # Depending on your route logic, might raise an error or 401, adjust accordingly
        self.assertEqual(response.status_code, 401)  # or 400 if you add validation

if __name__ == '__main__':
    unittest.main()
