![OH Crop Logo](https://user-images.githubusercontent.com/55028065/88461332-c5903a00-ce5f-11ea-8496-d12187350486.png)

## Contents
- [About](#about)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [Installation](#installation)
- [Endpoints](#endpoints)
- [Running the Tests](#running-the-tests)
- [End to End Testing](#end-to-end-testing)
- [Built With](#built-with)
- [Contributors](#contributors)

## <a name="about"></a> About

Oh Crop! Back End is an API built using Python and Flask. This API was created to

### <a name="prerequisites"></a> Prerequisites

You will need to have the following in order to run this app on your local machine.

```
Pip 20.1.1
Python3 3.8.4
Flask 1.1.2
```

## <a name="getting-started"></a> Getting Started

Follow the steps below to get you a copy of the project up and running on your local machine for development and testing purposes.

1. Clone this repo onto your local machine

2. Run the following commands in your terminal to get the code up and running on your local machine

- Make sure to run each of these without the $

```
$ pip install -r requirements.txt
$ alembic upgrade head
```


### <a name="installation"></a> Installation

Follow the steps below to view this app locally

Step 1:
    Start up your virtual environment by running the following command
    - Make sure you have completed the steps in the [getting started](#getting-started) section
```
$ . venv/bin/activate
```

Step 2:
    Start the local rails server by running the following command
```
$ flask run
```

Step 3:
  View the website locally by visiting http://localhost:5000/

  Note: All of the endpoints in the [endpoint](#endpoints) section can be run locally

## <a name="endpoints"></a> Endpoints

Here are some end points and request response examples to get you started.

## GET Endpoints:
__Motivational message__
This is the home page endpoint with some sample text to ensure that the app is working as expected

```
oh-crop-be.herokuapp.com/api/v1/
```

__All Plants__
This endpoint returns all plant object in the database

```
oh-crop-be.herokuapp.com/api/v1/plants
```

__Meet a random plant__
This endpoint returns a random plant from the database

```
Request:
https://oh-crop-be.herokuapp.com/api/v1/plants/meet

Response:
{
    "id": 15,
    "plant_image": "https://c1.peakpx.com/wallpaper/736/669/216/appetite-avacado-avo-avocado-wallpaper-preview.jpg",
    "plant_type": "Avocado"
```

__Get plant by ID (Plant Info)__
This endpoint requires an ID to be passed in and it will return information about that plant
```
Request:
https://oh-crop-be.herokuapp.com/api/v1/plants/2

Response:
{
    "annual?": "Perennial",
    "days_between_water": 3,
    "days_to_harvest_from_seed": 50,
    "id": 2,
    "lighting": "Full Sun",
    "plant_image": "https://cdn.pixabay.com/photo/2019/05/29/19/04/tomatoes-4238247_960_720.jpg",
    "plant_type": "Cherry Tomato",
    "root_depth_in": 12
}
```

Note: Add a plant ID to the end. In the example above the plants ID is `2`

__Plant Search__
```
Request:
https://oh-crop-be.herokuapp.com/api/v1/plants/search?q=tomato

Response:
[
    {
        "id": 1,
        "plant_image": "https://skitterphoto.com/photos/skitterphoto-1901-default.jpg",
        "plant_type": "Better Boy Tomato"
    },
    {
        "id": 2,
        "plant_image": "https://cdn.pixabay.com/photo/2019/05/29/19/04/tomatoes-4238247_960_720.jpg",
        "plant_type": "Cherry Tomato"
    },
    {
        "id": 3,
        "plant_image": "https://live.staticflickr.com/2591/3816942238_e669d597f7_w.jpg",
        "plant_type": "Roma Tomato"
    }
]
```

Note: will need to pass query params: {q: <search term>}

Note: Search term is not case sensitive and will search within all plant types

## POST Endpoints:
__Add Plant to Garden__
```
Request:
https://oh-crop-be.herokuapp.com/api/v1/garden?plant_id=4&plant_name=Terry

Response:
{
    "harvest_date": "Fri, 23 Oct 2020 00:00:00 GMT",
    "plant_id": 4,
    "plant_name": "Terry"
}
```

Note: will need to pass query params for the ID of the plant being added being added and the unique name the user will assign to the plant: {plant_id: 4, plant_name: Terry}


## <a name="running-the-tests"></a> Running the tests

__To run the entire test suite on your local machine run the following command__
```
$ pytest
```


__To run a specific test file run the following command__

```
$ python3 <file_path>
```

Note: Your file path may look something like `tests/test_endpoint.py`

### <a name="end-to-end-testing"></a> End to End Testing

These tests were written to check that the API endpoints were working as well as checking that the correct data is returned. Edge cases were also tested, for example we tested that when adding a plant to a garden the `date_to_harvest` is calculated, but if the plant is not one that can be harvested (ex. a cactus) it should return null.

__API Test Example__
```
def test_api_can_add_plant_to_garden(self):
    zeke = Plant(plant_type='Cherry Tomato',image='jim_photo.jpg',lighting='Full Sun',water_frequency=3,harvest_time=50,root_depth=12,annual="Annual")
    agatha = Plant(plant_type='Roma Tomato',image='agatha_photo.jpg',lighting='Full Sun',water_frequency=2,harvest_time=60,root_depth=12,annual="Annual")
    dan = Plant(plant_type='Cactus',image='cactus_dan.jpg',lighting='Full Sun',water_frequency=7,harvest_time=None,root_depth=8,annual="Annual")
    db.session.add_all([zeke, agatha, dan])
    db.session.commit()

    harvest_date = (datetime.now() + timedelta(days=50))
    parsed_harvest_date = harvest_date.strftime("%a, %d %b %Y")
    res = self.client().post('/api/v1/garden?plant_id=1&plant_name=Ezekiel')
    self.assertEqual(res.status_code, 201)
    self.assertIn("Ezekiel", str(res.data))
    self.assertIn("{} 00:00:00 GMT".format(parsed_harvest_date), str(res.data))
```

```
def test_api_can_add_plant_to_garden_with_no_harvest_date(self):
    zeke = Plant(plant_type='Cherry Tomato',image='jim_photo.jpg',lighting='Full Sun',water_frequency=3,harvest_time=50,root_depth=12,annual="Annual")
    dan = Plant(plant_type='Cactus',image='cactus_dan.jpg',lighting='Full Sun',water_frequency=7,harvest_time=None,root_depth=8,annual="Annual")
    db.session.add_all([zeke, dan])
    db.session.commit()

    res = self.client().post('/api/v1/garden?plant_id={}&plant_name=Marjorie'.format(dan.id))
    self.assertEqual(res.status_code, 201)
    self.assertIn("Marjorie", str(res.data))
    self.assertIn("null", str(res.data))
```

## <a name="built-with"></a> Built With

* [Flask](https://flask.palletsprojects.com/en/1.1.x/) - The web framework used
* [SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) - The object relational mapper used

## <a name="contributors"></a> Contributors

* [**Mike Hernandez**](https://github.com/mikez321)
* [**Kelsha Darby**](https://github.com/kelshadarby)
