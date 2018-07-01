# Gateway Service

Overview :bike:
========

* Gateway Service: It is the main entry point of the application. It provides information like list of bikes, bike data, trip data.
It also sends message to the message broker, in this case RabbitMQ, for location update on the two other services.




Starting and Stopping Services
==============================

* To launch the gateway service, from the gateway folder, run:
```
$ python manage.py runserver
```

* To stop the services, type `Ctl+c` on the keyboard.




APIs and Documentation
======================

## Gateway Service (port 8080)

The service is used as a gateway to route requests to the concerned service and to receive the response from that service. This service listen on port 8080.  

These are the different actions perform by the service:
* Return the list of all the bikes from database.
* Given a bike ID, return the corresponding bike.
* Given a bike ID, start a trip if the corresponding bike is not already in use and return the newly created trip ID.
* End a trip, make the associated bike available again and return the trip to the user.
* Send an event to the message broker, RabbitMQ in this case . This event is consumed by the other services to update the bike location but also to add the point to the trip history of locations.



**Return the list of all the bikes from database.**  
* `http://127.0.0.1:8080`  

GET /  
Returns a list of all bikes.  


```json
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

  .......... output truncated ...............
  ```


**Given a bike ID, return the corresponding bike.**  
* `http://127.0.0.1:8080\<id>`  
Depending on the bike status (ie. bike in use or not)  

GET /5b3429a54042be787bd6636  
Returns new trip ID.  

```json
    New trip ID	"5b37bc08b07c1a0ac4cd1120"
```
`or`  

GET /5b3429a54042be787bd6636  
Returns the specified bike.  

```json
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


**Given a bike ID, start a trip if the corresponding bike is not already in use and return the newly created trip id.**
* `http://127.0.0.1:8080/5b34cf89b07c1a1785db92d6`  

GET /5b34299e4042be787bd66362  
Returns the new trip id.  


```json
    New trip ID	"5b37c71eb07c1a0ac37f6db9"
```


**End a trip, make the associated bike available again and return the trip to the user.**  
* `http://127.0.0.1:8080/5b37c71eb07c1a0ac37f6db9`  


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

## Gateway Producer
The producer run on the gateway service and send events to the message broker. Those events are consumed by the other two services to update the bike location and add the point to the trip history.  

Kombu, the RabbitMQ client run as deamon on different thread on the flash server and listen to event sent to the gateway service on this uri:  
* http://127.0.0.1:8080/event  

POST /event
Return ack message

```bash
curl -i -X POST -H "Content-Type: application/json" -d "@event.json" http://127.0.0.1:8080/event
```

You will find `event.json` file in the project root folder. Run the curl command from the same directory to send the event.  

Event received  by the Gateway service is instantaneously sent to the broker and published to all the subscribers.  
