docker run -d -p 5672:5672 --hostname my-rabbit --name some-rabbit rabbitmq:3

mongoimport --collection bikes --db zoov --file bikes_db.json --jsonArray

celery -A tasks worker --loglevel=info

