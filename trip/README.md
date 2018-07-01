# Trip Service

Overview :bike:
========

* Trip Service: It takes a bike ID and starts a trip if the corresponding bike is not already in use and return the newly created trip ID. It ends a trip , make the associated bike available and return the trip to the user.




Starting and Stopping Services
==============================

* To launch the trip service, from the trip folder, run:
```
$ python manage.py runserver
```

* To stop the services, type `Ctl+c` on the keyboard.




APIs and Documentation
======================

## Trip Service (port 8082)

This service is used to get all the trips information and a speficied trip by ID. When a bike ID is provided, it start a trip if the correspnding bike is not in use and return the newly created trip ID.
Also, it end a trip and make the associated bike available again and return the trip to the user. It return information such as trip ID, bike ID, locations, start_at, end_at, status.


**To get all the trip in the database:**  
* `http://127.0.0.1:8082`  

GET /  
Returns a list of trips  

```json
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

.......... output truncated ...............
```


**To lookup by trip ID:**
* `http://127.0.0.1:8082/5b34cf89b07c1a1785db92d6`

GET /5b34cf89b07c1a1785db92d6  
Returns the specified trip  

```json
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

**To start a trip, provide bike ID:**  
* `http://127.0.0.1:8082:/start/5b34299e4042be787bd66362`  

GET /5b34299e4042be787bd66362  
Returns the new trip ID.  

```json
    New trip ID	"5b37c71eb07c1a0ac37f6db9"
```

**To end the trip and return the info to the user, provide the trip ID:**  
* `http://127.0.0.1:8082/end/5b37c71eb07c1a0ac37f6db9`  

GET /5b37c71eb07c1a0ac37f6db9  
Returns the trip info  

```json
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



Messaging service: Kombu/RabbitMQ
=================================
In this case, the message broker used is RabbitMQ. Kombu, a messaging library for Python is used as client to connect to the broker. It provides a high-level interface for the AMQ protocol used by RabbitMQ.  

Refer to the main README.md for the setup and configuration.  


## Trip Consumer
* The Trip service runs the Kombu consumer as deamon on a different thread to listen to event sent by the producer.  


The event is used by the service to update the bike location.  

Starting the server autoamatically starts the consumer deamon. The debugging output in the treminal help tracking the deamon.