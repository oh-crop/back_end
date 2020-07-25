# Oh Crop! Back End
##Get Endpoints:
__Motivational message__
```
oh-crop-be.herokuapp.com/api/v1/
```

__All Plants__
```
oh-crop-be.herokuapp.com/api/v1/plants
```

__Meet a random plant__
```
oh-crop-be.herokuapp.com/api/v1/plants/meet
```

__Get plant by ID__
```
oh-crop-be.herokuapp.com/api/v1/plants/2
```

Note: add a plant ID to the end... in the above example, plant ID = 2

__Plant Search__
```
oh-crop-be.herokuapp.com/api/v1/plants/search?q=tomato
```

Note: will need to pass query params: {q: <search term>}

Note: Search term is not case sensitive and will search within all plant types

##Post Endpoints:
__Add Plant to Garden__
```
oh-crop-be.herokuapp.com/api/v1/garden?plant_id=1&plant_name=Ezekiel
```

Note: will need to pass query params for the ID of the plant being added being added and the unique name the user will assign to the plant: {plant_id: 1, plant_name: Ezekiel}
