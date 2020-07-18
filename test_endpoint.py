import unittest
import os
import json
from app import create_app, db

class EndpointTestCase(unittest.TestCase):
    """This class represents the test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client

    def test_api_can_get_a_dummy_endpoint(self):
        """Test API can get a dummy string (GET request)."""
        res = self.client().get('/')
        self.assertEqual(res.status_code, 200)
        self.assertIn("I need to go take a shower so I can't tell if I'm crying or not.", str(res.data))

# Execute test
if __name__ == "__main__":
    unittest.main()
