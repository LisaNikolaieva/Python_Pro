simple flask app with celery

docker run -d -p 5672:5672 -p 15672:15672 rabbitmq:3-management

default management creds:

username: guest

password: guest

celery -A celery_worker worker --loglevel=INFO --purge --pool=solo

Postgress

https://hub.docker.com/_/postgres/

docker run --name some-postgres -e POSTGRES_PASSWORD=example -d -p 5432:5432 postgres


Migrations

alembic init alembic

alembic revision -m "first" --autogenerate

alembic upgrade head
