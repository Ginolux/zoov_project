docker run -d --restart=always -p 5672:5672 --hostname my-rabbit --name some-rabbit rabbitmq:3

docker run -d --restart=always -p 5672:5672 --hostname my-rabbit --name some-rabbit -p 8888:15672 rabbitmq:3-management

mongoimport --collection bikes --db zoov --file bikes_db.json --jsonArray

docker run --restart=always -p 27017:27017 -v /home/$USER/mongodbdata:/data/db mongo

celery -A tasks worker --loglevel=info

