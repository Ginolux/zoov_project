docker run -d --restart=always -p 5672:5672 --hostname my-rabbit --name some-rabbit rabbitmq:3

docker run -d --restart=always -p 5672:5672 --hostname my-rabbit --name some-rabbit -p 8888:15672 rabbitmq:3-management

mongoimport --collection bikes --db zoov --file bikes_db.json --jsonArray

docker run --restart=always -p 27017:27017 -v /home/$USER/mongodbdata:/data/db mongo

curl -i -X POST -H "Content-Type: application/json" -d "@event.json" http://127.0.0.1:8080/event

gunicorn -w 4 -b 0.0.0.0:8080 manage:app &


