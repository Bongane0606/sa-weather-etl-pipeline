"""Flask dashboard unit tests: no running database or API key required."""
import sys
import unittest
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'dashboard_api'))
import app as dashboard


class DashboardApiTests(unittest.TestCase):
    def setUp(self):
        dashboard.app.config['TESTING'] = True
        self.client = dashboard.app.test_client()

    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<html', response.data.lower())

    @patch.object(dashboard, 'query', return_value=[{'ok': 1}])
    def test_health_connected(self, mocked):
        response = self.client.get('/api/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'database': 'connected', 'status': 'ok'})

    @patch.object(dashboard, 'query', side_effect=Exception('connection failed'))
    def test_health_unavailable(self, mocked):
        response = self.client.get('/api/health')
        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.get_json()['status'], 'degraded')

    @patch.object(dashboard, 'query', return_value=[{'city': 'Durban', 'province': 'KwaZulu-Natal'}])
    def test_cities(self, mocked):
        response = self.client.get('/api/cities')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()[0]['city'], 'Durban')

    @patch.object(dashboard, 'query', return_value=[{'total_records': 3, 'cities': 1}])
    def test_summary_city_filter_is_parameterized(self, mocked):
        response = self.client.get('/api/summary?city=Durban')
        self.assertEqual(response.status_code, 200)
        sql, params = mocked.call_args.args
        self.assertIn('WHERE city = %s', sql)
        self.assertEqual(params, ('Durban',))

    @patch.object(dashboard, 'query', return_value=[])
    def test_latest_empty_result(self, mocked):
        response = self.client.get('/api/latest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [])

    @patch.object(dashboard, 'query', return_value=[])
    def test_history_default_limit(self, mocked):
        response = self.client.get('/api/history')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(mocked.call_args.args[1], (200,))

    @patch.object(dashboard, 'query', return_value=[])
    def test_history_limit_clamped(self, mocked):
        self.client.get('/api/history?city=Cape%20Town&limit=5000')
        self.assertEqual(mocked.call_args.args[1], ('Cape Town', 1000))
        self.client.get('/api/history?limit=-3')
        self.assertEqual(mocked.call_args.args[1], (1,))

    def test_history_invalid_limit(self):
        response = self.client.get('/api/history?limit=not-a-number')
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.get_json())

    def test_serialize_database_types(self):
        self.assertEqual(dashboard.serialize(Decimal('22.78')), 22.78)
        self.assertEqual(dashboard.serialize(datetime(2026, 10, 30, 9, 15)), '2026-10-30T09:15:00')
        self.assertEqual(dashboard.serialize('Durban'), 'Durban')


if __name__ == '__main__':
    unittest.main()
