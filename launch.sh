#! /usr/bin/zsh

rm database.db
gunicorn --bind 127.0.0.1:8080 main:app >access.log 2>error.log &!
rq worker --worker-ttl 600 --with-scheduler > redis.log 2>redis-error.log &!