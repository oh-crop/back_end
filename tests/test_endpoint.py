import unittest
import os
import json
from app import create_app, db
from app.models import Plant

class EndpointTestCase(unittest.TestCase):
    """This class represents the test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_api_can_get_a_dummy_endpoint(self):
        """Test API can get a dummy string (GET request)."""
        res = self.client().get('/')
        self.assertEqual(res.status_code, 200)
        self.assertIn("I need to go take a shower so I can't tell if I'm crying or not.", str(res.data))

    def test_api_can_get_a_plant_by_id(self):
        # add two plants
        andy = Plant(name='Andrew', plant_type='Better Boy Tomato',image='https://skitterphoto.com/photos/skitterphoto-1901-default.jpg',lighting='Full Sun', water_frequency=7, harvest_time=70, root_depth=24, annual=False)
        jimmy = Plant(name='Jimothy',plant_type='Cherry Tomato',image='https://cdn.pixabay.com/photo/2019/05/29/19/04/tomatoes-4238247_960_720.jpg',lighting='Full Sun',water_frequency=3,harvest_time=50,root_depth=12,annual=False)
        db.session.add_all([andy, jimmy])
        db.session.commit()

        # get plant
        response = self.client.get(
            '/plants/{}'.format(andy.id))
        self.assertEqual(response.status_code, 200)
        # json_response = json.loads(response.get_data(as_text=True))
        # self.assertEqual(json_response['name'], 'Andrew')
        # response = self.client.get(
        #     '/api/v1/users/{}'.format(jimmy.id),
        #     headers=self.get_api_headers('susan@example.com', 'dog'))
        # self.assertEqual(response.status_code, 200)
        # json_response = json.loads(response.get_data(as_text=True))
        # self.assertEqual(json_response['username'], 'susan')

# Execute test
if __name__ == "__main__":
    unittest.main()
