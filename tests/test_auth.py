import unittest
import json
from app import create_app

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def test_login_success(self):
        resp = self.client.post('/auth/login', json={"username":"admin", "password":"password123"})
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertIn('access_token', data)

    def test_login_failure(self):
        resp = self.client.post('/auth/login', json={"username":"admin", "password":"wrongpass"})
        self.assertEqual(resp.status_code, 401)
