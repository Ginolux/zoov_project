# zoov_project

## Microservices backend with Flask, MongoDB, Kombu/RabbitMQ


Overview
========

This project is a test to demonstrate the use of microvervices to achieve something similar to what are been developed at Zoov.

The application is powered by 3 microservices, all of them written in Python 3 using Flask.

* Gateway Service: It is the main entry point of the application. It provides information like list of bikes, bike data, trip data.
It also sends message to the message broker, in this case RabbitMQ, for location update on the two other services.
* Bike Service: It provides the list of all bikes and return a bike data if the id is given. It also consumes event sent by the gateway to update the bikes location.
* Trip Service: It takes a bike id and starts a trip if the corresponding bike is not already in use and return the newly created trip id. It ends a trip , make the associated bike available and return the trip to the user.



Requirements
============

* This project uses python 3
* The virtual environment requirements are in "requirements.txt"
* The database used is MongoDB 2.6.10
* RabbitMQ 3.7.6 is the message broker used to manage events sent across services. 



Install
========

* To install python 3 on Debian/Ubuntu system:
<code>
$ sudo apt install python3-devel
</code>

* Install the virtual environment on Debian/Ubuntu system:
<code>
$ pip install virtualenv
</code>
or 
<code>
$ sudo apt install virtualenv
</code>
* To create a virtual environment:
Ex: 
<code>
$ virtualenv -p python3 venv
</code>
* To install all the required modules:
First activate the virtual environment `source venv/bin/activate` and then install the modules.
<code>
$ pip install -r requirements.txt
</code>



Starting and Stopping Services
==============================

* To launch the services, from each service folder, run:
<code>
$ python manage.py runserver
</code>

* To stop the services, type `Ctl+c` on the keyboard



APIs and Documentation
======================

## Gateway Service (port 8080)

The service is used as a gateway to route request to the concerned service and receive the response from that service. It provides the informations return by the other services such as bike id, location, trip id and other information.


* To lookup all the bikes in the database, go to:
`http://127.0.0.1:8080`

    **GET /**
    **Returns a list of all bikes.**
```
    {
        "_id": {
            "$oid": "5b34299e4042be787bd66362"
        }, 
        "location": {
            "coordinates": [
            2.286146, 
            48.826802
            ], 
            "type": "Point"
        }, 
        "status": 1
    },
```
  .......... output truncated ...............


* To lookup by id:
`http://127.0.0.1:8080\<id>`
Depending on the bike status (ie. bike in use or not),

    **GET /5b3429a54042be787bd6636**
    **Returns new trip id.**
```
    New trip ID	"5b37bc08b07c1a0ac4cd1120"
```
`or` 

    GET /5b3429a54042be787bd6636
    Returns the specified bike.
```
    {
        "location": {
            "type": "Point",
            "coordinates": [
                2.286146,
                48.826802
            ]
        },
        "_id": {
            "$oid": "5b3429a54042be787bd66365"
        },
        "status": 0
    }
```

## Bike Service (port 8081)

This service is used to get a list of bikes and a bike information.


* To lookup all the bikes, type: 
`http://127.0.0.1:8081`

    **GET /**
    **Returns a list of all bikes.**
```
    {
        "_id": {
            "$oid": "5b34299e4042be787bd66362"
        }, 
        "location": {
        "coordinates": [
            2.286146, 
            48.826802
        ], 
        "type": "Point"
        }, 
        "status": 1
    }, 
```
.......... output truncated ...............


* To lookup by id:
`http://127.0.0.1:8081\<id>`

    **GET /**
    **Return the specified bike**
```
    {
        "_id": {
            "$oid": "5b34fa850164c925a23a7477"
        }, 
        "location": {
        "coordinates": [
            2.286146, 
            48.826802
        ], 
        "type": "Point"
        }, 
        "status": 1.0
    }
```


## Trip Service (port 8082)

This service is used to get all the trips information and a speficied trip by id. When a bike id is provided, it start a trip if the correspnding bike is not in use and return the newly created trip id.
Also, it end a trip and make the associated bike available again and return the trip to the user. It return information such as trip id, bike id, locations, start_at, end_at, status.


* To get all the trip in the database:
`http://127.0.0.1:8082`

    **GET /**
    **Returns a list of trips**
```
    {
        "_id": {
            "$oid": "5b3429c9b07c1a09861b5da1"
        }, 
        "bike_id": "5b34299e4042be787bd66362", 
        "ended_at": "2018-06-28 00:32:33.207766", 
        "locations": [
            {
            "coordinates": [
                2.286146, 
                48.826802
            ], 
            "type": "Point"
            }
        ], 
        "started_at": "2018-06-28 00:20:25.073834", 
        "status": 1
    } 
```
.......... output truncated ...............


* To lookup by trip id:
`http://127.0.0.1:8082/5b34cf89b07c1a1785db92d6`

    **GET /5b34cf89b07c1a1785db92d6**
    **Returns the specified trip**
```
    {
        "_id": {
            "$oid": "5b34cf89b07c1a1785db92d6"
        }, 
        "bike_id": "5b3429a44042be787bd66364", 
        "ended_at": "2018-06-28 12:09:26.388318", 
        "locations": [
        {
            "coordinates": [
            2.286146, 
            48.826802
            ], 
            "type": "Point"
        }
        ], 
        "started_at": "2018-06-28 12:07:37.470175", 
        "status": 1
    }
```

* To start a trip, provide bike id:
`http://127.0.0.1:8082:/5b34299e4042be787bd66362`

    **GET /5b34299e4042be787bd66362**
    **Returns the new trip id.**
```
    New trip ID	"5b37c71eb07c1a0ac37f6db9"
```

* To end the trip and return the info to the user, provide the trip id:
`http://127.0.0.1:8082/5b37c71eb07c1a0ac37f6db9`

    **GET /5b37c71eb07c1a0ac37f6db9**
    **Returns the trip info**
```
    {
        "_id": {
            "$oid": "5b37c71eb07c1a0ac37f6db9"
        }, 
        "bike_id": "5b34299e4042be787bd66362", 
        "ended_at": "2018-06-30 18:13:40.680738", 
        "locations": [
            {
            "coordinates": [
                2.286146, 
                48.826802
            ], 
            "type": "Point"
            }
        ], 
        "started_at": "2018-06-30 18:08:30.415901", 
        "status": 1
    }
```


