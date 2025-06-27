import unittest
from app import create_app, db
from app.models import Asset
from datetime import datetime, timedelta

class AssetTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_asset(self):
        response = self.client.post('/assets', json={
            "name": "Test Asset",
            "service_time": (datetime.utcnow() + timedelta(minutes=10)).isoformat(),
            "expiration_time": (datetime.utcnow() + timedelta(minutes=20)).isoformat()
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn("id", data)

    def test_get_assets(self):
        response = self.client.get('/assets')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)

    def test_run_checks_no_assets(self):
        response = self.client.get('/run-checks')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["notifications_created"], 0)
        self.assertEqual(data["violations_created"], 0)

if __name__ == '__main__':
    unittest.main()
