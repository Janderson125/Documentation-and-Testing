import unittest
import json
from app import create_app, db
from app.models import Mechanic
from flask_jwt_extended import create_access_token

class MechanicsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app().test_client()
        self.access_token = None

        # Setup app context and test DB (adjust based on your app structure)
        with create_app().app_context():
            db.create_all()

        with create_app().app_context():
            self.access_token = create_access_token(identity="admin")

    def tearDown(self):
        with create_app().app_context():
            db.drop_all()

    def test_get_mechanics_empty(self):
        response = self.app.get('/mechanics/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

    def test_create_mechanic_success(self):
        new_mechanic = {
            "name": "Test Mechanic",
            "specialty": "Brakes",
            "phone": "555-1234"
        }
        response = self.app.post('/mechanics/',
                                 data=json.dumps(new_mechanic),
                                 content_type='application/json',
                                 headers={"Authorization": f"Bearer {self.access_token}"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], new_mechanic['name'])

    def test_create_mechanic_unauthorized(self):
        new_mechanic = {
            "name": "Test Mechanic",
            "specialty": "Brakes"
        }
        response = self.app.post('/mechanics/',
                                 data=json.dumps(new_mechanic),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_create_mechanic_validation_error(self):
        invalid_mechanic = {
            "name": ""
        }
        response = self.app.post('/mechanics/',
                                 data=json.dumps(invalid_mechanic),
                                 content_type='application/json',
                                 headers={"Authorization": f"Bearer {self.access_token}"})
        self.assertEqual(response.status_code, 400)

    def test_get_mechanic_not_found(self):
        response = self.app.get('/mechanics/999')
        self.assertEqual(response.status_code, 404)

    def test_update_mechanic_success(self):
        with create_app().app_context():
            mechanic = Mechanic(name="Old Name", specialty="Oil Change")
            db.session.add(mechanic)
            db.session.commit()
            mechanic_id = mechanic.id

        updated_data = {"name": "New Name", "specialty": "Engine"}
        response = self.app.put(f'/mechanics/{mechanic_id}',
                                data=json.dumps(updated_data),
                                content_type='application/json',
                                headers={"Authorization": f"Bearer {self.access_token}"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], "New Name")

    def test_delete_mechanic_success(self):
        with create_app().app_context():
            mechanic = Mechanic(name="Delete Me", specialty="Tires")
            db.session.add(mechanic)
            db.session.commit()
            mechanic_id = mechanic.id

        response = self.app.delete(f'/mechanics/{mechanic_id}',
                                   headers={"Authorization": f"Bearer {self.access_token}"})
        self.assertEqual(response.status_code, 204)

    def test_delete_mechanic_not_found(self):
        response = self.app.delete('/mechanics/999',
                                   headers={"Authorization": f"Bearer {self.access_token}"})
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
