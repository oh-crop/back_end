import unittest
import os
import json
from app import create_app, db
from app.models import Plant, Garden, GardenPlant
from datetime import datetime, timedelta
import logging
import sys


class EndpointTestCase(unittest.TestCase):
    """Endpoint tests."""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        """Reset for next round of testing."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_api_can_get_welcome_endpoint(self):
        """Test API can get a dummy string (GET request)."""
        res = self.client().get('/api/v1/')
        self.assertEqual(res.status_code, 200)
        self.assertIn("I need to go take a shower so I can't tell if I'm crying or not.", str(res.data))

# Plant Endpoint Tests
    # Plant GET Requests
    def test_api_can_return_all_plants(self):
        zeke = Plant(plant_type='Cherry Tomato',
                     image='jim_photo.jpg',
                     lighting='Full Sun',
                     water_frequency=3,
                     harvest_time=50,
                     root_depth=12,
                     annual="Annual")
        dan = Plant(plant_type='Cactus',
                    image='cactus_dan.jpg',
                    lighting='Full Sun',
                    water_frequency=7,
                    harvest_time=None,
                    root_depth=8,
                    annual="Annual")
        agatha = Plant(plant_type='Roma Tomato',
                       image='agatha_photo.jpg',
                       lighting='Full Sun',
                       water_frequency=2,
                       harvest_time=60,
                       root_depth=12,
                       annual="Annual")
        db.session.add_all([zeke, dan, agatha])
        db.session.commit()

        res = self.client().get('/api/v1/plants/')
        self.assertEqual(res.status_code, 200)

        json_response = json.loads(res.data)

        self.assertEqual(len(json_response), 3)

        self.assertEqual(zeke.id, json_response[0]['id'])
        self.assertEqual(zeke.image, json_response[0]['image'])
        self.assertEqual(dan.id, json_response[1]['id'])
        self.assertEqual(dan.image, json_response[1]['image'])
        self.assertEqual(agatha.id, json_response[2]['id'])
        self.assertEqual(agatha.image, json_response[2]['image'])

    def test_api_can_return_a_random_plant(self):
        zeke = Plant(plant_type='Cherry Tomato',
                     image='jim_photo.jpg',
                     lighting='Full Sun',
                     water_frequency=3,
                     harvest_time=50,
                     root_depth=12,
                     annual="Annual")
        dan = Plant(plant_type='Cactus',
                    image='cactus_dan.jpg',
                    lighting='Full Sun',
                    water_frequency=7,
                    harvest_time=None,
                    root_depth=8,
                    annual="Annual")
        agatha = Plant(plant_type='Roma Tomato',
                       image='agatha_photo.jpg',
                       lighting='Full Sun',
                       water_frequency=2,
                       harvest_time=60,
                       root_depth=12,
                       annual="Annual")
        db.session.add_all([zeke, dan, agatha])
        db.session.commit()

        res = self.client().get('/api/v1/plants/meet')
        self.assertEqual(res.status_code, 200)

        json_response = json.loads(res.data)

        self.assertIsNotNone(json_response['id'])
        self.assertIsNotNone(json_response['plant_type'])
        self.assertIsNotNone(json_response['plant_image'])

    def test_api_can_return_a_plant_by_id(self):
        jimmy = Plant(plant_type='Cherry Tomato',image='jim_photo.jpg',lighting='Full Sun',water_frequency=3,harvest_time=50,root_depth=12,annual="Annual")
        dan = Plant(plant_type='Cactus',image='cactus_dan.jpg',lighting='Full Sun',water_frequency=7,harvest_time=None,root_depth=8,annual="Annual")
        db.session.add_all([jimmy, dan])
        db.session.commit()
        res = self.client().get('/api/v1/plants/{}'.format(jimmy.id))
        self.assertEqual(res.status_code, 200)

        json_response = json.loads(res.data)

        self.assertNotEqual(dan.id, json_response['id'])

        self.assertEqual(jimmy.id, json_response['id'])
        self.assertEqual(jimmy.plant_type, json_response['plant_type'])
        self.assertEqual(jimmy.image, json_response['plant_image'])
        self.assertEqual(jimmy.lighting, json_response['lighting'])
        self.assertEqual(jimmy.water_frequency, json_response['days_between_water'])
        self.assertEqual(jimmy.harvest_time, json_response['days_to_harvest_from_seed'])
        self.assertEqual(jimmy.root_depth, json_response['root_depth_in'])
        self.assertEqual(jimmy.annual, json_response['lifecycle'])

    def test_api_can_search_for_a_plant_type(self):
        jimmy = Plant(plant_type='Cherry Tomato',image='jim_photo.jpg',lighting='Full Sun',water_frequency=3,harvest_time=50,root_depth=12,annual="Annual")
        agatha = Plant(plant_type='Roma Tomato',image='agatha_photo.jpg',lighting='Full Sun',water_frequency=2,harvest_time=60,root_depth=12,annual="Annual")
        dan = Plant(plant_type='Cactus',image='cactus_dan.jpg',lighting='Full Sun',water_frequency=7,harvest_time=None,root_depth=8,annual="Annual")
        db.session.add_all([jimmy, agatha, dan])
        db.session.commit()
        res = self.client().get('/api/v1/plants/search?q=tomato')
        self.assertEqual(res.status_code, 200)

        json_response = json.loads(res.data)

        self.assertEqual(len(json_response), 2)

        self.assertEqual(jimmy.id, json_response[0]['id'])
        self.assertEqual(jimmy.plant_type, json_response[0]['plant_type'])
        self.assertEqual(jimmy.image, json_response[0]['plant_image'])
        self.assertEqual(agatha.id, json_response[1]['id'])
        self.assertEqual(agatha.plant_type, json_response[1]['plant_type'])
        self.assertEqual(agatha.image, json_response[1]['plant_image'])

        self.assertNotIn(dan.id, json_response)
        self.assertNotIn(dan.plant_type, json_response)
        self.assertNotIn(dan.image, json_response)

    def test_api_can_search_for_a_plant_is_alphabetical(self):
        jimmy = Plant(plant_type='Cherry Tomato',image='jim_photo.jpg',lighting='Full Sun',water_frequency=3,harvest_time=50,root_depth=12,annual="Annual")
        agatha = Plant(plant_type='Roma Tomato',image='agatha_photo.jpg',lighting='Full Sun',water_frequency=2,harvest_time=60,root_depth=12,annual="Annual")
        dan = Plant(plant_type='Cactus',image='cactus_dan.jpg',lighting='Full Sun',water_frequency=7,harvest_time=None,root_depth=8,annual="Annual")
        db.session.add_all([jimmy, agatha, dan])
        db.session.commit()
        res = self.client().get('/api/v1/plants/search?q=a')
        self.assertEqual(res.status_code, 200)

        json_response = json.loads(res.data)
        # For easier readability, each plant type is listed in order below:
        # dan.plant_type: 'Cactus'
        # jimmy.plant_type: 'Cherry Tomato'
        # agatha.plant_type: 'Roma Tomato'

        self.assertEqual(dan.plant_type, json_response[0]['plant_type'])
        self.assertEqual(jimmy.plant_type, json_response[1]['plant_type'])
        self.assertEqual(agatha.plant_type, json_response[2]['plant_type'])

    def test_api_can_search_for_a_plant_type_sad_path(self):
        jimmy = Plant(plant_type='Cherry Tomato',image='jim_photo.jpg',lighting='Full Sun',water_frequency=3,harvest_time=50,root_depth=12,annual="Annual")
        agatha = Plant(plant_type='Roma Tomato',image='agatha_photo.jpg',lighting='Full Sun',water_frequency=2,harvest_time=60,root_depth=12,annual="Annual")
        dan = Plant(plant_type='Cactus',image='cactus_dan.jpg',lighting='Full Sun',water_frequency=7,harvest_time=None,root_depth=8,annual="Annual")
        db.session.add_all([jimmy, agatha, dan])
        db.session.commit()
        res = self.client().get('/api/v1/plants/search?q=elephant')
        self.assertEqual(res.status_code, 200)

        no_response_image = 'https://images.unsplash.com/reserve/unsplash_529f1a3f2f5ed_1.JPG'
        no_response_message = 'Oh Crop!  We did not find any plants called elephant.  Maybe try a different search term?'

        json_response = json.loads(res.data)

        self.assertEqual(len(json_response), 1)

        self.assertEqual(no_response_image, json_response[0]['plant_image'])
        self.assertEqual(no_response_message, json_response[0]['plant_type'])
        self.assertNotIn(jimmy.id, json_response)
        self.assertNotIn(jimmy.plant_type, json_response)
        self.assertNotIn(jimmy.image, json_response)
        self.assertNotIn(agatha.id, json_response)
        self.assertNotIn(agatha.plant_type, json_response)
        self.assertNotIn(agatha.image, json_response)
        self.assertNotIn(dan.id, json_response)
        self.assertNotIn(dan.plant_type, json_response)
        self.assertNotIn(dan.image, json_response)

# Garden Plant Endpoint Tests
    # Garden Plant GET Requests
    def test_api_can_return_msg_when_no_plants_are_in_garden(self):
        garden = Garden(id=1)
        zeke = Plant(plant_type='Cherry Tomato',image='jim_photo.jpg',lighting='Full Sun',water_frequency=3,harvest_time=50,root_depth=12,annual="Annual")
        dan = Plant(plant_type='Cactus',image='cactus_dan.jpg',lighting='Full Sun',water_frequency=7,harvest_time=None,root_depth=8,annual="Annual")
        agatha = Plant(plant_type='Roma Tomato',image='agatha_photo.jpg',lighting='Full Sun',water_frequency=2,harvest_time=60,root_depth=12,annual="Annual")
        db.session.add_all([zeke, dan, agatha, garden])
        db.session.commit()

        res = self.client().get('/api/v1/garden')
        self.assertEqual(res.status_code, 200)

        json_response = json.loads(res.data)

        self.assertEqual('You have no plants in your garden', json_response['info'])

    def test_api_can_return_all_plants_in_garden(self):
        garden = Garden(id=1)
        zeke = Plant(plant_type='Cherry Tomato',image='jim_photo.jpg',lighting='Full Sun',water_frequency=3,harvest_time=50,root_depth=12,annual="Annual")
        dan = Plant(plant_type='Cactus',image='cactus_dan.jpg',lighting='Full Sun',water_frequency=7,harvest_time=None,root_depth=8,annual="Annual")
        agatha = Plant(plant_type='Roma Tomato',image='agatha_photo.jpg',lighting='Full Sun',water_frequency=2,harvest_time=60,root_depth=12,annual="Annual")
        db.session.add_all([zeke, dan, agatha, garden])
        db.session.commit()

        res = self.client().post('/api/v1/garden?plant_id={}&plant_name=Ezekiel'.format(zeke.id))
        res = self.client().post('/api/v1/garden?plant_id={}&plant_name=Dan'.format(dan.id))

        res = self.client().get('/api/v1/garden')
        self.assertEqual(res.status_code, 200)

        json_response = json.loads(res.data)

        self.assertEqual(len(json_response), 2)

        self.assertEqual(zeke.id, json_response[0]['id'])
        self.assertEqual("Ezekiel", json_response[0]['plant_name'])
        self.assertEqual(dan.id, json_response[1]['id'])
        self.assertEqual("Dan", json_response[1]['plant_name'])

        self.assertNotEqual(agatha.id, json_response[0]['id'])
        self.assertNotEqual(agatha.id, json_response[1]['id'])


    def test_api_can_return_garden_plant_profile_page(self):
        garden = Garden(id=1)
        adrian = Plant(id=5, plant_type='Buckcherry',image='adrian_photo.jpg',lighting='Full Sun',water_frequency=5,harvest_time=50,root_depth=12,annual="Annual")
        db.session.add_all([adrian, garden])
        db.session.commit()
        add_adrian_res = self.client().post('/api/v1/garden?plant_id={}&plant_name=Adrian'.format(adrian.id))

        add_adrian_json = json.loads(add_adrian_res.data)
        gardenplant_id = add_adrian_json['garden_plant_id']

        profile_res = self.client().get('/api/v1/garden/plants/{}'.format(gardenplant_id))
        self.assertEqual(profile_res.status_code, 200)

        profile_json_response = json.loads(profile_res.data)

        today = datetime.now().strftime("%a, %B %d, %Y")
        harvest_date = (datetime.now() + timedelta(days=adrian.harvest_time)).strftime("%a, %B %d, %Y")
        remaining_harvest = ((datetime.now() + timedelta(days=adrian.harvest_time)) - datetime.now()).days

        self.assertEqual(gardenplant_id, profile_json_response['gardenplant_id'])
        self.assertEqual("Adrian", profile_json_response['plant_name'])
        self.assertEqual(today, profile_json_response['date_added'])
        self.assertEqual(today, profile_json_response['last_watered'])
        self.assertEqual(harvest_date, profile_json_response['harvest_date'])
        self.assertEqual(remaining_harvest, profile_json_response['days_until_harvest'])
        self.assertEqual(adrian.plant_type, profile_json_response['plant_type'])
        self.assertEqual(adrian.image, profile_json_response['image'])
        self.assertIsNotNone(profile_json_response['days_until_next_water'])

    def test_api_can_return_garden_plant_profile_page_with_no_harvest_date(self):
        garden = Garden(id=1)
        adrian = Plant(id=5, plant_type='Buckcherry',image='adrian_photo.jpg',lighting='Full Sun',water_frequency=5,harvest_time=None,root_depth=12,annual="Annual")
        db.session.add_all([adrian, garden])
        db.session.commit()
        add_adrian_res = self.client().post('/api/v1/garden?plant_id={}&plant_name=Adrian'.format(adrian.id))

        add_adrian_json = json.loads(add_adrian_res.data)
        gardenplant_id = add_adrian_json['garden_plant_id']

        profile_res = self.client().get('/api/v1/garden/plants/{}'.format(gardenplant_id))
        self.assertEqual(profile_res.status_code, 200)

        profile_json_response = json.loads(profile_res.data)

        today = datetime.now().strftime("%a, %B %d, %Y")

        self.assertEqual(gardenplant_id, profile_json_response['gardenplant_id'])
        self.assertEqual("Adrian", profile_json_response['plant_name'])
        self.assertEqual(today, profile_json_response['date_added'])
        self.assertEqual(today, profile_json_response['last_watered'])
        self.assertEqual("N/A", profile_json_response['harvest_date'])
        self.assertEqual("N/A", profile_json_response['days_until_harvest'])
        self.assertEqual(adrian.plant_type, profile_json_response['plant_type'])
        self.assertEqual(adrian.image, profile_json_response['image'])
        self.assertIsNotNone(profile_json_response['days_until_next_water'])

    # Garden Plant POST Requests
    def test_api_can_add_plant_to_garden(self):
        garden = Garden(id=1)
        zeke = Plant(plant_type='Cherry Tomato',image='jim_photo.jpg',lighting='Full Sun',water_frequency=3,harvest_time=50,root_depth=12,annual="Annual")
        agatha = Plant(plant_type='Roma Tomato',image='agatha_photo.jpg',lighting='Full Sun',water_frequency=2,harvest_time=60,root_depth=12,annual="Annual")
        dan = Plant(plant_type='Cactus',image='cactus_dan.jpg',lighting='Full Sun',water_frequency=7,harvest_time=None,root_depth=8,annual="Annual")
        db.session.add_all([zeke, agatha, dan, garden])
        db.session.commit()

        harvest_date = (datetime.now() + timedelta(days=50))
        parsed_harvest_date = harvest_date.strftime("%a, %B %d, %Y")
        res = self.client().post('/api/v1/garden?plant_id={}&plant_name=Ezekiel'.format(zeke.id))
        self.assertEqual(res.status_code, 201)

        json_response = json.loads(res.data)

        self.assertIsNotNone(json_response['garden_plant_id'])
        self.assertEqual(zeke.id, json_response['plant_id'])
        self.assertEqual(garden.id, json_response['garden_id'])
        self.assertEqual("Ezekiel", json_response['plant_name'])
        self.assertEqual(parsed_harvest_date, json_response['harvest_date'])

        self.assertNotEqual(agatha.id, json_response['plant_id'])
        self.assertNotEqual(dan.id, json_response['plant_id'])

    def test_api_can_add_plant_to_garden_with_no_harvest_date(self):
        garden = Garden(id=1)
        zeke = Plant(plant_type='Cherry Tomato',image='jim_photo.jpg',lighting='Full Sun',water_frequency=3,harvest_time=50,root_depth=12,annual="Annual")
        dan = Plant(plant_type='Cactus',image='cactus_dan.jpg',lighting='Full Sun',water_frequency=7,harvest_time=None,root_depth=8,annual="Annual")
        db.session.add_all([zeke, dan, garden])
        db.session.commit()

        res = self.client().post('/api/v1/garden?plant_id={}&plant_name=Cactus Dan'.format(dan.id))
        self.assertEqual(res.status_code, 201)

        json_response = json.loads(res.data)

        self.assertIsNotNone(json_response['garden_plant_id'])
        self.assertEqual(dan.id, json_response['plant_id'])
        self.assertEqual(garden.id, json_response['garden_id'])
        self.assertEqual("Cactus Dan", json_response['plant_name'])
        self.assertEqual("N/A", json_response['harvest_date'])

        self.assertNotEqual(zeke.id, json_response['plant_id'])

    # Garden Plant DELETE Requests
    def test_api_can_remove_a_plant_from_a_garden(self):
        garden = Garden(id=1)
        lincoln = Plant(plant_type='Lime',image='lincoln_photo.jpg',lighting='Full Sun',water_frequency=5,harvest_time=50,root_depth=12,annual="Annual")
        db.session.add_all([lincoln, garden])
        db.session.commit()
        res = self.client().post('/api/v1/garden?plant_id={}&plant_name=Lincoln'.format(lincoln.id))

        data_dict = json.loads(res.data)
        gardenplant_id = data_dict['garden_plant_id']

        res1 = self.client().get('/api/v1/garden')
        self.assertEqual(res1.status_code, 200)
        lincoln_in_garden_json_response = json.loads(res1.data)
        self.assertEqual("Lincoln", lincoln_in_garden_json_response[0]['plant_name'])
        self.assertEqual(lincoln.id, lincoln_in_garden_json_response[0]['id'])

        res2 = self.client().delete('/api/v1/garden/plants/{}'.format(gardenplant_id))
        self.assertEqual(res2.status_code, 202)
        lincoln_out_of_garden_json_response = json.loads(res2.data)
        self.assertEqual("Lincoln", lincoln_out_of_garden_json_response['plant_name'])
        self.assertEqual(gardenplant_id, lincoln_out_of_garden_json_response['gardenplant_id'])

        res3 = self.client().get('/api/v1/garden')
        self.assertEqual(res3.status_code, 200)
        no_plants_garden_json_response = json.loads(res3.data)
        self.assertEqual("You have no plants in your garden", no_plants_garden_json_response['info'])

    # Garden Plant PUT Requests
    def test_api_can_update_watering_information(self):
        garden = Garden(id=1)
        zeke = Plant(plant_type='Cherry Tomato',image='jim_photo.jpg',lighting='Full Sun',water_frequency=3,harvest_time=50,root_depth=12,annual="Annual")
        dan = Plant(id=5,plant_type='Cactus',image='cactus_dan.jpg',lighting='Full Sun',water_frequency=7,harvest_time=None,root_depth=8,annual="Annual")
        db.session.add_all([zeke, dan, garden])
        db.session.commit()


        res_zeke = self.client().post('/api/v1/garden?plant_id={}&plant_name=Ezekiel'.format(zeke.id))
        res_dan = self.client().post('/api/v1/garden?plant_id={}&plant_name=Dan'.format(dan.id))

        dan_json_response = json.loads(res_dan.data)
        zeke_json_response = json.loads(res_zeke.data)

        self.assertEqual("Dan", dan_json_response['plant_name'])

        water_res = self.client().put('/api/v1/garden/water?garden_plant_id={}'.format(dan_json_response['garden_plant_id']))
        self.assertEqual(water_res.status_code, 201)

        last_watered = datetime.now().strftime("%a, %B %d, %Y")
        next_water = (datetime.now() + timedelta(days=dan.water_frequency)).strftime("%a, %B %d, %Y")

        water_json_response = json.loads(water_res.data)

        self.assertEqual(dan_json_response['garden_plant_id'], water_json_response['id'])
        self.assertEqual(dan_json_response['plant_name'], water_json_response['name'])
        self.assertEqual(dan.plant_type, water_json_response['plant_type'])
        self.assertEqual(dan.water_frequency, water_json_response['water_frequency'])
        self.assertEqual(last_watered, water_json_response['last_watered'])
        self.assertEqual(next_water, water_json_response['next_water'])

        self.assertNotEqual(zeke_json_response['garden_plant_id'], water_json_response['id'])
        self.assertNotEqual(zeke_json_response['plant_name'], water_json_response['name'])
        self.assertNotEqual(zeke.plant_type, water_json_response['plant_type'])
        self.assertNotEqual(zeke.water_frequency, water_json_response['water_frequency'])
