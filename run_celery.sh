#!/bin/bash

docker run -d --rm --name demo-mail -p 8025:8025 -p  1025:1025 -d mailhog/mailhog
docker run -d --rm --name demo-rabbitmq -p 5672:5672 -d rabbitmq:3

echo "Esperando el inicio de rabbitmq ..." && sleep 20

celery -A demo worker -l info -B

docker rm -f demo-mail
docker rm -f demo-rabbitmq
