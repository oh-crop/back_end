import unittest
import os
import json
from app import create_app, db
from app.models import Plant, Garden
from datetime import datetime
from datetime import timedelta

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
        res = self.client().get('/api/v1/')
        self.assertEqual(res.status_code, 200)
        self.assertIn("I need to go take a shower so I can't tell if I'm crying or not.", str(res.data))

    def test_api_can_return_a_plant_by_id(self):
        jimmy = Plant(plant_type='Cherry Tomato',image='jim_photo.jpg',lighting='Full Sun',water_frequency=3,harvest_time=50,root_depth=12,annual="Annual")
        dan = Plant(plant_type='Cactus',image='cactus_dan.jpg',lighting='Full Sun',water_frequency=7,harvest_time=None,root_depth=8,annual="Annual")
        db.session.add_all([jimmy, dan])
        db.session.commit()
        res = self.client().get('/api/v1/plants/{}'.format(jimmy.id))
        self.assertEqual(res.status_code, 200)
        self.assertNotIn(dan.plant_type, str(res.data))
        self.assertIn(jimmy.plant_type, str(res.data))

    def test_api_can_search_for_a_plant_type(self):
        jimmy = Plant(plant_type='Cherry Tomato',image='jim_photo.jpg',lighting='Full Sun',water_frequency=3,harvest_time=50,root_depth=12,annual="Annual")
        agatha = Plant(plant_type='Roma Tomato',image='agatha_photo.jpg',lighting='Full Sun',water_frequency=2,harvest_time=60,root_depth=12,annual="Annual")
        dan = Plant(plant_type='Cactus',image='cactus_dan.jpg',lighting='Full Sun',water_frequency=7,harvest_time=None,root_depth=8,annual="Annual")
        db.session.add_all([jimmy, agatha, dan])
        db.session.commit()
        res = self.client().get('/api/v1/plants/search?q=tomato')
        self.assertEqual(res.status_code, 200)
        self.assertNotIn(dan.plant_type, str(res.data))
        self.assertIn(jimmy.plant_type, str(res.data))
        self.assertIn(agatha.plant_type, str(res.data))

    def test_api_can_add_plant_to_garden(self):
        garden = Garden(id=1)
        zeke = Plant(plant_type='Cherry Tomato',image='jim_photo.jpg',lighting='Full Sun',water_frequency=3,harvest_time=50,root_depth=12,annual="Annual")
        agatha = Plant(plant_type='Roma Tomato',image='agatha_photo.jpg',lighting='Full Sun',water_frequency=2,harvest_time=60,root_depth=12,annual="Annual")
        dan = Plant(plant_type='Cactus',image='cactus_dan.jpg',lighting='Full Sun',water_frequency=7,harvest_time=None,root_depth=8,annual="Annual")
        db.session.add_all([zeke, agatha, dan, garden])
        db.session.commit()

        harvest_date = (datetime.now() + timedelta(days=50))
        parsed_harvest_date = harvest_date.strftime("%a, %d %b %Y")
        res = self.client().post('/api/v1/garden?plant_id=1&plant_name=Ezekiel')
        self.assertEqual(res.status_code, 201)
        self.assertIn("Ezekiel", str(res.data))
        self.assertIn("{} 00:00:00 GMT".format(parsed_harvest_date), str(res.data))

    def test_api_can_add_plant_to_garden_with_no_harvest_date(self):
        garden = Garden(id=1)
        zeke = Plant(plant_type='Cherry Tomato',image='jim_photo.jpg',lighting='Full Sun',water_frequency=3,harvest_time=50,root_depth=12,annual="Annual")
        dan = Plant(plant_type='Cactus',image='cactus_dan.jpg',lighting='Full Sun',water_frequency=7,harvest_time=None,root_depth=8,annual="Annual")
        db.session.add_all([zeke, dan, garden])
        db.session.commit()

        res = self.client().post('/api/v1/garden?plant_id={}&plant_name=Marjorie'.format(dan.id))
        self.assertEqual(res.status_code, 201)
        self.assertIn("Marjorie", str(res.data))
        self.assertIn("null", str(res.data))

    def test_api_can_return_all_plants_in_garden(self):
        res = self.client().get('/api/v1/garden/1')
        self.assertEqual(res.status_code, 200)


# Execute test
if __name__ == "__main__":
    unittest.main()
