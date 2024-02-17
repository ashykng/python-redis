import unittest
from json import loads
from PyInMemStore import app

class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True


    def test_set_key(self):
        response = self.app.put('/set/test_key/test_value')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), 'set successfully')


    def test_get_key(self):
        self.app.put('/set/test_key/test_value')
        response = self.app.get('/get/test_key')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), 'test_value')


    def test_get_key_ttl(self):
        self.app.put('/set/test_key/test_value', query_string={'expire': 10})
        response = self.app.get('/get/ttl/test_key')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(int(response.data.decode()) <= 10)


    def test_delete_key(self):
        self.app.put('/set/test_key/test_value')
        response = self.app.delete('/del/test_key')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), 'Key deleted successfully')


def test_get_all_keys(self):
    self.app.put('/set/test_key1/test_value1')
    self.app.put('/set/test_key2/test_value2')
    response = self.app.get('/get_all_keys')
    self.assertEqual(response.status_code, 200)
    response_data = loads(response.data.decode())
    expected_keys = ['test_key1: test_value1', 'test_key2: test_value2']
    for expected_key in expected_keys:
        self.assertIn(expected_key, response_data)


    def test_delete_all_keys(self):
        self.app.put('/set/test_key1/value1')
        self.app.put('/set/test_key2/value2')
        response = self.app.delete('/del_all_keys')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), 'All keys deleted successfully')


if __name__ == '__main__':
    unittest.main()