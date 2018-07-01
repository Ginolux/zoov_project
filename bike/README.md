# Bike Service

Overview :bike:
========

* Bike Service: It provides the list of all bikes and return a bike data if the id is given. It also consumes event sent by the gateway to update the bikes location.




Starting and Stopping Services
==============================

* To launch the bike service, from the bike folder, run:
```
$ python manage.py runserver
```

* To stop the services, type `Ctl+c` on the keyboard.




APIs and Documentation
======================

## Bike Service (port 8081)

This service is used to get a list of bikes and a bike information. This service listen on port 8081 and exposes two endpoints.

* Return the list of all the bikes from database.
* Given a bike ID, return the corresponding bike.



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


**To lookup by ID:**  
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



Messaging service: Kombu/RabbitMQ
=================================
In this case, the message broker used is RabbitMQ. Kombu, a messaging library for Python is used as client to connect to the broker. It provides a high-level interface for the AMQ protocol used by RabbitMQ.  

Refer to the main README.md for the setup and configuration.  


## Bike Consumer
* The Bike service runs the Kombu consumer as deamon on a different thread to listen to event sent by the producer.  


The event is used by the service to update the bike location.  

Starting the server autoamatically starts the consumer deamon. The debugging output in the treminal help tracking the deamon.


