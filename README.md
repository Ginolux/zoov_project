

Microservices backend with Flask, MongoDB, Kombu/RabbitMQ
===========================================================

### Demo
Link to start the demo :arrow_forward: http://52.212.180.26:8080/     

RabbitMQ management interface on http://52.212.180.26:8888, with the username and password of guest / guest 



Overview :bike:
========

This project is a test to demonstrate the use of microservices to achieve something similar to what have been developed at Zoov.

The application is powered by 3 microservices, all written in Python 3 using Flask.

* Gateway Service: It is the main entry point of the application. It provides information like list of bikes, bike data and trip data.
It also sends message to the message broker, in this case RabbitMQ which is for update the bike location on the two other services.
* Bike Service: It provides the list of all bikes. It returns a bike info if the associated ID is given. It also consumes event sent by the gateway to update the bikes location.
* Trip Service: It takes a bike ID and starts a trip if the corresponding bike is not already in use and return the newly created trip ID. It ends a trip , make the associated bike available and return the trip to the user.



Requirements
============

* This project uses python 3.
* The project requirements are in "requirements.txt" file.
* The database used is MongoDB 2.6.10.
* RabbitMQ 3.7.6 is the message broker used to manage events sent across the services. 



Install
========

* To install python 3 on Debian/Ubuntu system:
```
$ sudo apt install python3-devel
```

* To install the virtual environment on Debian/Ubuntu system:
```
$ pip install virtualenv
```
or 

```
$ sudo apt install virtualenv
```

* To create a virtual environment:
Ex: 
```
$ virtualenv -p python3 venv
```

* To install all the required modules:
First activate the virtual environment `source venv/bin/activate` and then install the modules.

```
$ pip install -r requirements.txt
```



Starting and Stopping Services
==============================

* To launch the services, from each service folder, run:
```
$ python manage.py runserver
```

* To stop the services, type `Ctl+c` on the keyboard



APIs and Documentation
======================

## Gateway Service (port 8080)

The service is used as a gateway to route request to the concerned service and receive the response from that service. It provides the informations return by the other services such as bike ID, location, trip ID and other information.


**To lookup all the bikes in the database, go to:**  
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
```
  .......... output truncated ...............


**To lookup by ID:**  
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



## Bike Service (port 8081)

This service is used to get a list of bikes and a bike information.


**To lookup all the bikes, type:**  
* `http://127.0.0.1:8081`  

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


**To lookup by id:**  
* `http://127.0.0.1:8081\<id>`  

GET /  
Return the specified bike   

```json
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

This service is use to get all the trips information and a specify trip by ID. When a bike ID is provided, it start a trip if the corresponding bike is not in use and return the newly created trip ID.
Also, it end a trip and make the associated bike available again and return the trip to the user. It return information such as trip ID, bike ID and locations, start_at, end_at and status.


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


**To lookup by trip id:**
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

**To start a trip, provide bike id:**  
* `http://127.0.0.1:8082:/5b34299e4042be787bd66362`  

GET /5b34299e4042be787bd66362  
Returns the new trip ID.  

```json
    New trip ID	"5b37c71eb07c1a0ac37f6db9"
```

**To end the trip and return the info to the user, provide the trip id:**  
* `http://127.0.0.1:8082/5b37c71eb07c1a0ac37f6db9`  

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

## Setup
RabbitMQ is deployed in docker for fast deployment. Here is the link to setup the doker container: https://hub.docker.com/_/rabbitmq/  
  
The management web interface run on port 8888 on the localhost with the default username and password of guest / guest.

### Producer
The producer run on the gateway service and send events to the message broker. Those events are consumed by the other two services to update the bike location and add the point to the trip history.  

Kombu, the RabbitMQ client run as deamon on different thread on the flash server and listen to event sent to the gateway service on this uri:  
* http://127.0.0.1:8080/event  

POST /event
Return ack message

```bash
curl -i -X POST -H "Content-Type: application/json" -d "@event.json" http://127.0.0.1:8080/event
```

You will find `event.json` file in the project root folder. Run the curl command from the same directory.  

Event received is instantaniouly sent to the broker and published to all the subscribers.  


### Consumers
* Each, Bike service and Trip service run the Kombu consumer as deamon on a different thread to listen to event sent by the producer.  


The event is used by the two services to update the bike location and the trips history of locations.


## Configuation
* AMQP: "amqp://localhost:5672/"
* Producer: Deamon run on Gateway service
* Consumer: Deamon run on both Bike and Trip services
* Queue: name="gateway-queue"
* Message: It comes from the `event.json` file, sent from the producer to the consumers through RabbitMQ
* Connection: It is a TCP connection between the services and RabbitMQ broker
* Channel: A virtual channel is created for each client when publishing or consuming messages
* Exchange: name="gateway-exchange", type="fanout". A fanout exchange routes messages to all of the queues that are bound to it. 


