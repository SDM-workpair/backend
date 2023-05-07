docker-compose build
docker-compose run backend alembic revision --autogenerate -m "Add cascade contraint into mr_member"
docker-compose run backend alembic upgrade head