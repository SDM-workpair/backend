docker-compose build
docker-compose run backend alembic revision --autogenerate -m "Recreate all table"
docker-compose run backend alembic upgrade head